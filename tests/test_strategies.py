"""Per-strategy behaviour tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from chunkwise import chunk

FIXTURES = Path(__file__).parent / "fixtures"


def test_fixed_respects_max_tokens() -> None:
    document = "a" * 1000
    chunks = chunk(document, strategy="fixed", max_tokens=100, overlap=0)
    assert all(len(c.text) <= 100 for c in chunks)
    assert "".join(c.text for c in chunks) == document


def test_fixed_overlap_widens_backwards() -> None:
    document = "abcdefghijklmnopqrstuvwxyz" * 10
    chunks = chunk(document, strategy="fixed", max_tokens=20, overlap=5)
    assert len(chunks) > 1
    for prev, nxt in zip(chunks, chunks[1:], strict=False):
        assert nxt.start < prev.end


def test_fixed_rejects_invalid_overlap() -> None:
    with pytest.raises(ValueError):
        chunk("some text", strategy="fixed", max_tokens=10, overlap=10)


def test_recursive_prefers_paragraph_breaks() -> None:
    document = (FIXTURES / "sample.txt").read_text()
    chunks = chunk(document, strategy="recursive", max_tokens=200, overlap=0)
    assert len(chunks) >= 1
    for c in chunks:
        assert document[c.start : c.end] == c.text


def test_markdown_tags_heading_path() -> None:
    document = (FIXTURES / "sample.md").read_text()
    chunks = chunk(document, strategy="markdown", max_tokens=80, overlap=0)
    assert any(c.heading_path for c in chunks)
    install_chunks = [c for c in chunks if c.heading_path and c.heading_path[-1] == "Install"]
    assert install_chunks


def test_markdown_keeps_code_fence_intact() -> None:
    document = (FIXTURES / "sample.md").read_text()
    chunks = chunk(document, strategy="markdown", max_tokens=15, overlap=0)
    for c in chunks:
        assert c.text.count("```") % 2 == 0


def test_unknown_strategy_raises() -> None:
    with pytest.raises(ValueError):
        chunk("text", strategy="nonexistent")
