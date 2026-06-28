from __future__ import annotations

import re
from typing import Sequence

import requests

from rag_app.config import settings


SYSTEM_PROMPT = """You are a policy helpdesk assistant. Answer only from the supplied policy context.
If the context does not support the answer, say: I can only answer from Code 5 Developers documents.
Keep the answer concise. Do not include citation markers in the answer text because citations are shown separately."""

REFUSAL_MESSAGE = "I can only answer from Code 5 Developers documents."


def generate_answer(question: str, contexts: Sequence[dict]) -> str:
    if not contexts:
        return REFUSAL_MESSAGE
    if settings.groq_api_key:
        return groq_answer(question, contexts)
    return extractive_answer(question, contexts)


def groq_answer(question: str, contexts: Sequence[dict]) -> str:
    context_text = "\n\n".join(
        f"[{item['title']} | {item['chunk_id']}]\n{item['text']}" for item in contexts
    )
    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Question: {question}\n\nPolicy context:\n{context_text}",
            },
        ],
        "temperature": 0.1,
        "max_tokens": settings.max_answer_tokens,
    }
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.groq_api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=settings.request_timeout,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def extractive_answer(question: str, contexts: Sequence[dict]) -> str:
    terms = important_terms(question)
    best_sentences: list[str] = []
    for item in contexts[:3]:
        sentences = re.split(r"(?<=[.!?])\s+", item["text"])
        ranked = sorted(
            sentences,
            key=lambda sentence: sum(term in sentence.lower() for term in terms),
            reverse=True,
        )
        for sentence in ranked[:2]:
            clean = clean_sentence(sentence)
            if clean and clean not in best_sentences and len(clean.split()) > 5:
                best_sentences.append(f"{clean} [{item['title']} | {item['chunk_id']}]")
            if len(best_sentences) >= 4:
                break
        if len(best_sentences) >= 4:
            break
    if not best_sentences or not has_overlap(question, contexts):
        return REFUSAL_MESSAGE
    return " ".join(best_sentences)


def clean_sentence(sentence: str) -> str:
    kept_lines = []
    for line in sentence.splitlines():
        clean = line.strip()
        if not clean:
            continue
        if clean.startswith("#"):
            continue
        if re.search(r"\bPage\s+\d+\b", clean):
            continue
        if re.search(r"(Policy|Manual|Handbook|Guide|Playbook|Runbook|Plan)$", clean):
            continue
        kept_lines.append(clean)
    sentence = " ".join(kept_lines)
    sentence = re.sub(r"\s+", " ", sentence)
    return sentence.strip()


def important_terms(text: str) -> set[str]:
    stop = {
        "a",
        "an",
        "and",
        "are",
        "about",
        "can",
        "do",
        "for",
        "how",
        "i",
        "is",
        "of",
        "on",
        "the",
        "to",
        "what",
        "when",
        "where",
        "who",
    }
    terms = set()
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        if word in stop:
            continue
        terms.add(word)
        if len(word) > 3 and word.endswith("s"):
            terms.add(word[:-1])
    return terms


def has_overlap(question: str, contexts: Sequence[dict]) -> bool:
    terms = important_terms(question)
    if not terms:
        return False
    haystack_terms = important_terms(" ".join(item["text"].lower() for item in contexts[:3]))
    return bool(terms.intersection(haystack_terms))
