from rag_app.app import create_app


class FakeStore:
    def stats(self):
        return {"collection": "test", "chunks": 1, "path": "/tmp/test"}

    def search(self, question, k):
        if "world cup" in question.lower():
            return []
        return [
            {
                "title": "Software Delivery Lifecycle Policy",
                "chunk_id": "delivery:abc123",
                "source_path": "policies/01-software-delivery-lifecycle.md",
                "heading": "Delivery Phases",
                "text": "The delivery workflow uses standard phases: discovery, solution design, implementation, quality assurance, user acceptance testing, deployment, and support transition.",
                "score": 0.92,
                "distance": 0.08,
            }
        ]


def test_health_endpoint(monkeypatch):
    monkeypatch.setattr("rag_app.app.VectorStore", lambda: FakeStore())
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_chat_returns_citations(monkeypatch):
    monkeypatch.setattr("rag_app.app.VectorStore", lambda: FakeStore())
    monkeypatch.setattr(
        "rag_app.rag.generate_answer",
        lambda question, contexts: "Standard phases are discovery, solution design, implementation, quality assurance, user acceptance testing, deployment, and support transition. [Software Delivery Lifecycle Policy | delivery:abc123]",
    )
    app = create_app()
    client = app.test_client()

    response = client.post("/chat", json={"question": "What is the delivery workflow?"})
    data = response.get_json()

    assert response.status_code == 200
    assert "quality assurance" in data["answer"]
    assert "delivery:abc123" not in data["answer"]
    assert data["citations"][0]["title"] == "Software Delivery Lifecycle Policy"
    assert data["snippets"]


def test_chat_refuses_out_of_corpus(monkeypatch):
    monkeypatch.setattr("rag_app.app.VectorStore", lambda: FakeStore())
    app = create_app()
    client = app.test_client()

    response = client.post("/chat", json={"question": "Who won the 2018 World Cup?"})
    data = response.get_json()

    assert response.status_code == 200
    assert data["answer"] == "I can only answer from Code 5 Developers documents."
    assert data["citations"] == []
    assert data["snippets"] == []
