from __future__ import annotations

from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request, send_from_directory

from rag_app.config import settings
from rag_app.documents import SUPPORTED_SUFFIXES, extract_title, parse_file
from rag_app.rag import RagPipeline
from rag_app.vector_store import VectorStore


def create_app() -> Flask:
    app = Flask(__name__)
    store = VectorStore()
    pipeline = RagPipeline(store)

    @app.get("/")
    def index():
        return render_template(
            "index.html",
            documents=list_library_documents(),
            stats=safe_stats(store),
            model=settings.llm_model,
        )

    @app.get("/library")
    def library():
        return render_template("library.html", documents=list_library_documents())

    @app.get("/library/<path:filename>")
    def library_document(filename: str):
        document = find_library_document(filename)
        if not document:
            abort(404)
        content = ""
        if document["type"] != "pdf":
            content = parse_file(settings.policy_dir / filename)
        return render_template("document.html", document=document, content=content)

    @app.get("/documents/<path:filename>")
    def document_file(filename: str):
        if not find_library_document(filename):
            abort(404)
        return send_from_directory(settings.policy_dir, filename)

    @app.post("/chat")
    def chat():
        payload = request.get_json(silent=True) or {}
        question = str(payload.get("question", "")).strip()
        response = pipeline.answer(question)
        return jsonify(response.to_dict())

    @app.get("/health")
    def health():
        stats = safe_stats(store)
        return jsonify(
            {
                "status": "ok" if stats["chunks"] > 0 else "degraded",
                "index_available": stats["chunks"] > 0,
                **stats,
            }
        )

    return app


def safe_stats(store: VectorStore) -> dict:
    try:
        return store.stats()
    except Exception as exc:
        return {"collection": settings.collection_name, "chunks": 0, "path": str(settings.chroma_dir), "error": str(exc)}


def list_library_documents() -> list[dict]:
    documents = []
    for path in sorted(settings.policy_dir.glob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        title = title_for_path(path)
        documents.append(
            {
                "filename": path.name,
                "title": title,
                "type": path.suffix.lower().lstrip("."),
                "size_kb": max(1, round(path.stat().st_size / 1024)),
                "view_url": f"/library/{path.name}",
                "file_url": f"/documents/{path.name}",
            }
        )
    return documents


def find_library_document(filename: str) -> dict | None:
    safe_name = Path(filename).name
    for document in list_library_documents():
        if document["filename"] == safe_name:
            return document
    return None


def title_for_path(path: Path) -> str:
    try:
        text = parse_file(path)
        return extract_title(text, path)
    except Exception:
        return path.stem.replace("-", " ").title()


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
