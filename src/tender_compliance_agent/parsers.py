from __future__ import annotations

from pathlib import Path

from tender_compliance_agent.models import DocumentChunk, SourceLocation

SUPPORTED_SUFFIXES = {".md", ".txt"}


def load_text_chunks(input_path: Path) -> list[DocumentChunk]:
    files = _iter_supported_files(input_path)
    chunks: list[DocumentChunk] = []

    for file_path in files:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        current_heading: str | None = None
        for index, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("#"):
                current_heading = stripped.lstrip("#").strip() or current_heading
            if not stripped:
                continue
            chunks.append(
                DocumentChunk(
                    text=stripped,
                    source=SourceLocation(
                        file_path=str(file_path),
                        line_number=index,
                        heading=current_heading,
                    ),
                )
            )

    return chunks


def _iter_supported_files(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path] if input_path.suffix.lower() in SUPPORTED_SUFFIXES else []

    return sorted(
        path
        for path in input_path.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )
