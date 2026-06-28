from __future__ import annotations

import argparse

from rag_app.config import settings
from rag_app.documents import chunk_documents, load_documents
from rag_app.vector_store import VectorStore


def build_index(reset: bool = True) -> dict:
    documents = load_documents(settings.policy_dir)
    chunks = chunk_documents(documents)
    store = VectorStore()
    if reset:
        store.reset()
    store.add_chunks(chunks)
    return {"documents": len(documents), "chunks": len(chunks), **store.stats()}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the policy vector index.")
    parser.add_argument("--no-reset", action="store_true", help="Append instead of rebuilding.")
    args = parser.parse_args()
    stats = build_index(reset=not args.no_reset)
    print(
        f"Indexed {stats['documents']} documents into {stats['chunks']} chunks "
        f"at {stats['path']}."
    )


if __name__ == "__main__":
    main()

