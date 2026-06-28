from rag_app.rag import RagPipeline


class FakeStore:
    def search(self, question, k):
        return [
            {
                "title": "Maintenance and Support Policy",
                "chunk_id": "support:1",
                "source_path": "policies/05-maintenance-and-support.md",
                "heading": "Response Targets",
                "text": "Critical production incidents are acknowledged within 30 minutes during covered support hours.",
                "score": 0.88,
                "distance": 0.12,
            }
        ]


def test_retrieval_answer_contains_expected_policy(monkeypatch):
    monkeypatch.setattr(
        "rag_app.rag.generate_answer",
        lambda question, contexts: "Critical production incidents are acknowledged within 30 minutes.",
    )
    response = RagPipeline(FakeStore()).answer("How fast are critical incidents acknowledged?")

    assert "30 minutes" in response.answer
    assert response.citations[0]["title"] == "Maintenance and Support Policy"
