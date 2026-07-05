from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    policy_dir: Path = ROOT_DIR / "policies"
    chroma_dir: Path = Path(os.getenv("CHROMA_DIR", ROOT_DIR / ".chroma"))
    collection_name: str = os.getenv("CHROMA_COLLECTION", "policy_chunks")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "chroma-onnx-all-MiniLM-L6-v2")
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
    top_k: int = int(os.getenv("TOP_K", "5"))
    max_answer_tokens: int = int(os.getenv("MAX_ANSWER_TOKENS", "450"))
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "45"))


settings = Settings()
