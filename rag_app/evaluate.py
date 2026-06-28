from __future__ import annotations

import json
import statistics
from pathlib import Path

from rag_app.config import ROOT_DIR
from rag_app.llm import REFUSAL_MESSAGE
from rag_app.rag import RagPipeline


QUESTIONS_PATH = ROOT_DIR / "eval" / "questions.jsonl"
RESULTS_PATH = ROOT_DIR / "eval" / "results.json"


def load_questions(path: Path = QUESTIONS_PATH) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def evaluate() -> dict:
    pipeline = RagPipeline()
    rows = []
    for item in load_questions():
        response = pipeline.answer(item["question"]).to_dict()
        citation_titles = {citation["title"] for citation in response["citations"]}
        expected_titles = set(item["expected_sources"])
        citation_hit = bool(citation_titles.intersection(expected_titles))
        grounded = response["answer"] != REFUSAL_MESSAGE
        rows.append(
            {
                **item,
                **response,
                "citation_hit": citation_hit,
                "grounded_auto_check": grounded,
            }
        )
    latencies = [row["latency_ms"] for row in rows]
    results = {
        "question_count": len(rows),
        "citation_accuracy_auto": round(sum(row["citation_hit"] for row in rows) / len(rows), 3),
        "groundedness_auto": round(
            sum(row["grounded_auto_check"] for row in rows) / len(rows), 3
        ),
        "latency_ms_p50": int(statistics.median(latencies)),
        "latency_ms_p95": int(sorted(latencies)[max(0, int(len(latencies) * 0.95) - 1)]),
        "rows": rows,
        "manual_review_note": (
            "Auto metrics are a first pass. Final groundedness and citation accuracy "
            "should be manually reviewed against retrieved snippets before submission."
        ),
    }
    RESULTS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results


def main() -> None:
    results = evaluate()
    print(json.dumps({k: v for k, v in results.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
