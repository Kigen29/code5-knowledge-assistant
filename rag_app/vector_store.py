from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from rag_app.config import ROOT_DIR, settings
from rag_app.documents import Chunk


class Embedder:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.embedding_model
        self._embedding_function = None

    @property
    def embedding_function(self):
        if self._embedding_function is None:
            from chromadb.utils import embedding_functions

            cache_dir = ROOT_DIR / ".cache" / "chroma" / "onnx_models" / "all-MiniLM-L6-v2"
            embedding_functions.ONNXMiniLM_L6_V2.DOWNLOAD_PATH = cache_dir
            self._embedding_function = embedding_functions.ONNXMiniLM_L6_V2()
        return self._embedding_function

    def encode(self, texts: list[str]) -> list[list[float]]:
        vectors = self.embedding_function(texts)
        return [list(vector) for vector in vectors]


class VectorStore:
    def __init__(self, persist_dir: Path | None = None, collection_name: str | None = None):
        self.persist_dir = persist_dir or settings.chroma_dir
        self.collection_name = collection_name or settings.collection_name
        self.embedder = Embedder()
        self._client = None
        self._collection = None

    @property
    def client(self):
        if self._client is None:
            import chromadb
            from chromadb.config import Settings

            self.persist_dir.mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(
                path=str(self.persist_dir),
                settings=Settings(anonymized_telemetry=False),
            )
        return self._client

    @property
    def collection(self):
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                self.collection_name, metadata={"hnsw:space": "cosine"}
            )
        return self._collection

    def reset(self) -> None:
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass
        self._collection = self.client.get_or_create_collection(
            self.collection_name, metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(self, chunks: list[Chunk]) -> None:
        if not chunks:
            return
        embeddings = self.embedder.encode([chunk.text for chunk in chunks])
        self.collection.add(
            ids=[chunk.chunk_id for chunk in chunks],
            documents=[chunk.text for chunk in chunks],
            metadatas=[
                {
                    "doc_id": chunk.doc_id,
                    "title": chunk.title,
                    "source_path": chunk.source_path,
                    "heading": chunk.heading,
                }
                for chunk in chunks
            ],
            embeddings=embeddings,
        )

    def search(self, query: str, k: int | None = None) -> list[dict]:
        query_embedding = self.embedder.encode([query])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k or settings.top_k,
            include=["documents", "metadatas", "distances"],
        )
        items: list[dict] = []
        ids = results.get("ids", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        for chunk_id, text, metadata, distance in zip(ids, documents, metadatas, distances):
            item = dict(metadata)
            item.update(
                {
                    "chunk_id": chunk_id,
                    "text": text,
                    "distance": float(distance),
                    "score": round(1.0 - float(distance), 4),
                }
            )
            items.append(item)
        return items

    def count(self) -> int:
        return int(self.collection.count())

    def stats(self) -> dict:
        count = self.count()
        return {"collection": self.collection_name, "chunks": count, "path": str(self.persist_dir)}


def chunk_to_dict(chunk: Chunk) -> dict:
    return asdict(chunk)
