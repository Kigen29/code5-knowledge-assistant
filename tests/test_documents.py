from pathlib import Path

from rag_app.documents import chunk_documents, load_documents


def test_ingestion_creates_chunks_with_metadata(tmp_path: Path):
    policy_dir = tmp_path / "policies"
    policy_dir.mkdir()
    (policy_dir / "delivery.md").write_text(
        "# Delivery Policy\n\n## Review\nCode must be reviewed before release.",
        encoding="utf-8",
    )

    docs = load_documents(policy_dir)
    chunks = chunk_documents(docs)

    assert len(docs) == 1
    assert chunks
    assert chunks[0].title == "Delivery Policy"
    assert chunks[0].source_path.endswith("delivery.md")
    assert chunks[0].chunk_id.startswith("delivery:")
