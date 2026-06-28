from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SUPPORTED_SUFFIXES = {".md", ".txt", ".html", ".htm", ".pdf"}


@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    source_path: str
    text: str


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    source_path: str
    heading: str
    text: str


def load_documents(policy_dir: Path) -> list[Document]:
    docs: list[Document] = []
    for path in sorted(policy_dir.glob("**/*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED_SUFFIXES:
            continue
        text = parse_file(path)
        clean = clean_text(text)
        if not clean:
            continue
        docs.append(
            Document(
                doc_id=path.stem,
                title=extract_title(clean, path),
                source_path=str(path.relative_to(policy_dir.parent)),
                text=clean,
            )
        )
    return docs


def parse_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8")
    if suffix in {".html", ".htm"}:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        return soup.get_text("\n")
    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    raise ValueError(f"Unsupported file type: {path.suffix}")


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_title(text: str, path: Path) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#"):
            return line.lstrip("#").strip()
        if line:
            return line[:90]
    return path.stem.replace("-", " ").title()


def chunk_documents(
    documents: Iterable[Document], max_words: int = 650, overlap_words: int = 90
) -> list[Chunk]:
    chunks: list[Chunk] = []
    for doc in documents:
        sections = split_by_heading(doc.text)
        chunk_number = 0
        for heading, section_text in sections:
            for piece in window_words(section_text, max_words, overlap_words):
                chunk_number += 1
                digest = hashlib.sha1(
                    f"{doc.doc_id}:{chunk_number}:{heading}:{piece[:120]}".encode("utf-8")
                ).hexdigest()[:10]
                chunks.append(
                    Chunk(
                        chunk_id=f"{doc.doc_id}:{chunk_number:04d}:{digest}",
                        doc_id=doc.doc_id,
                        title=doc.title,
                        source_path=doc.source_path,
                        heading=heading,
                        text=piece,
                    )
                )
    return chunks


def split_by_heading(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^(#{1,3})\s+(.+)$", text))
    if not matches:
        return [("General", text)]
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        heading = match.group(2).strip()
        section_text = text[start:end].strip()
        if section_text:
            sections.append((heading, section_text))
    return sections


def window_words(text: str, max_words: int, overlap_words: int) -> list[str]:
    words = text.split()
    if len(words) <= max_words:
        return [text.strip()]
    pieces = []
    step = max(1, max_words - overlap_words)
    for start in range(0, len(words), step):
        piece = " ".join(words[start : start + max_words]).strip()
        if piece:
            pieces.append(piece)
        if start + max_words >= len(words):
            break
    return pieces
