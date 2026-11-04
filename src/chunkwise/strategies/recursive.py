"""Recursive strategy: falls back through a separator chain to find natural breaks.

Breaks on the coarsest boundary that fits the budget — paragraphs, then lines,
then sentences, then words. This is the default strategy.
"""

from __future__ import annotations

import re

from .._spans import find_boundary, materialize
from ..types import Chunk, Tokenizer

SEPARATOR_CHAIN = [
    re.compile(r"\n\s*\n"),  # paragraphs
    re.compile(r"\n"),  # lines
    re.compile(r"(?<=[.!?])\s+"),  # sentences
    re.compile(r"\s+"),  # words
]


def _best_split_point(document: str, start: int, limit: int) -> int:
    """Find the best separator-aligned split point within (start, limit]."""
    window = document[start:limit]
    for separator in SEPARATOR_CHAIN:
        matches = list(separator.finditer(window))
        if matches:
            last = matches[-1]
            split = start + last.end()
            if split > start:
                return split
    return limit


def chunk_recursive(
    document: str,
    max_tokens: int,
    overlap: int,
    tokenizer: Tokenizer,
) -> list[Chunk]:
    """Split document on the coarsest separator that keeps each chunk within budget."""
    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    if overlap < 0 or overlap >= max_tokens:
        raise ValueError("overlap must be in [0, max_tokens)")

    spans: list[tuple[int, int]] = []
    start = 0
    n = len(document)
    while start < n:
        hard_limit = find_boundary(document, start, max_tokens, tokenizer)
        end = _best_split_point(document, start, hard_limit) if hard_limit < n else hard_limit
        if end <= start:
            end = hard_limit
        spans.append((start, end))
        if end >= n:
            break
        back_start = find_boundary(document, start, max_tokens - overlap, tokenizer)
        start = max(min(back_start, end), start + 1)

    return materialize(document, spans)
