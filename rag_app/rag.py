from __future__ import annotations

import time
import re
from dataclasses import dataclass

from rag_app.config import settings
from rag_app.llm import REFUSAL_MESSAGE, generate_answer, has_overlap
from rag_app.vector_store import VectorStore


@dataclass
class RagResponse:
    answer: str
    citations: list[dict]
    snippets: list[dict]
    latency_ms: int

    def to_dict(self) -> dict:
        return {
            "answer": self.answer,
            "citations": self.citations,
            "snippets": self.snippets,
            "latency_ms": self.latency_ms,
        }


class RagPipeline:
    def __init__(self, store: VectorStore | None = None):
        self.store = store or VectorStore()

    def answer(self, question: str) -> RagResponse:
        started = time.perf_counter()
        clean_question = question.strip()
        if not clean_question:
            return RagResponse("Please enter a policy question.", [], [], 0)
        contexts = self.store.search(clean_question, settings.top_k)
        if not contexts or not has_overlap(clean_question, contexts):
            answer = REFUSAL_MESSAGE
            contexts = []
        else:
            answer = generate_answer(clean_question, contexts)
        latency_ms = int((time.perf_counter() - started) * 1000)
        return RagResponse(
            answer=clean_answer_text(answer),
            citations=build_citations(contexts),
            snippets=build_snippets(contexts),
            latency_ms=latency_ms,
        )


def build_citations(contexts: list[dict]) -> list[dict]:
    citations = []
    seen = set()
    for item in contexts:
        key = (item["title"], item["chunk_id"])
        if key in seen:
            continue
        seen.add(key)
        citations.append(
            {
                "title": item["title"],
                "chunk_id": item["chunk_id"],
                "source_path": item.get("source_path", ""),
                "heading": item.get("heading", ""),
                "score": item.get("score"),
                "relevance": relevance_label(item.get("score")),
            }
        )
    return citations


def relevance_label(score: float | None) -> str:
    if score is None:
        return "retrieved"
    return f"{max(0, min(100, round(score * 100)))}% match"


def clean_answer_text(answer: str) -> str:
    answer = re.sub(r"\s*\[[^\[\]]+\s+\|\s+[^\[\]]+\]", "", answer)
    answer = re.sub(r"\s{2,}", " ", answer)
    return answer.strip()


def build_snippets(contexts: list[dict]) -> list[dict]:
    snippets = []
    for item in contexts:
        text = " ".join(item["text"].split())
        snippets.append(
            {
                "title": item["title"],
                "chunk_id": item["chunk_id"],
                "heading": item.get("heading", ""),
                "source_path": item.get("source_path", ""),
                "score": item.get("score"),
                "relevance": relevance_label(item.get("score")),
                "snippet": text[:420] + ("..." if len(text) > 420 else ""),
            }
        )
    return snippets
