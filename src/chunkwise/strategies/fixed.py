"""Fixed-window strategy: hard windows of N tokens with configurable overlap."""

from __future__ import annotations

from .._spans import find_boundary, materialize
from ..types import Chunk, Tokenizer


def chunk_fixed(
    document: str,
    max_tokens: int,
    overlap: int,
    tokenizer: Tokenizer,
) -> list[Chunk]:
    """Split document into hard windows of at most max_tokens, overlapping by `overlap` tokens.

    Overlap widens a chunk backwards into real preceding text rather than
    gluing on a copied prefix, preserving the offset invariant.
    """
    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    if overlap < 0 or overlap >= max_tokens:
        raise ValueError("overlap must be in [0, max_tokens)")

    spans: list[tuple[int, int]] = []
    start = 0
    n = len(document)
    while start < n:
        end = find_boundary(document, start, max_tokens, tokenizer)
        spans.append((start, end))
        if end >= n:
            break
        back_start = find_boundary(document, start, max_tokens - overlap, tokenizer)
        start = max(back_start, start + 1)

    return materialize(document, spans)
