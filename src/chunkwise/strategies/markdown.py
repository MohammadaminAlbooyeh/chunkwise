"""Markdown-aware strategy: keeps fenced code blocks intact, tags chunks with heading paths."""

from __future__ import annotations

import re

from .._spans import find_boundary
from ..types import Chunk, Tokenizer

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
FENCE_RE = re.compile(r"^```.*?$.*?^```$", re.MULTILINE | re.DOTALL)


def _code_fence_spans(document: str) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in FENCE_RE.finditer(document)]


def _heading_path_at(document: str, offset: int) -> tuple[str, ...]:
    stack: list[tuple[int, str]] = []
    for match in HEADING_RE.finditer(document):
        if match.start() > offset:
            break
        level = len(match.group(1))
        title = match.group(2).strip()
        stack = [(lvl, t) for lvl, t in stack if lvl < level]
        stack.append((level, title))
    return tuple(title for _, title in stack)


def chunk_markdown(
    document: str,
    max_tokens: int,
    overlap: int,
    tokenizer: Tokenizer,
) -> list[Chunk]:
    """Split markdown document, never breaking a fenced code block, tagging heading paths."""
    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    if overlap < 0 or overlap >= max_tokens:
        raise ValueError("overlap must be in [0, max_tokens)")

    fences = _code_fence_spans(document)
    spans: list[tuple[int, int]] = []
    start = 0
    n = len(document)

    while start < n:
        hard_limit = find_boundary(document, start, max_tokens, tokenizer)

        for fence_start, fence_end in fences:
            if fence_start < hard_limit < fence_end:
                hard_limit = fence_end
                break

        end = max(hard_limit, start + 1)
        end = min(end, n)
        spans.append((start, end))
        if end >= n:
            break
        if overlap == 0:
            start = end
        else:
            back_start = find_boundary(document, start, max_tokens - overlap, tokenizer)
            start = max(min(back_start, end), start + 1)

    return [
        Chunk(
            text=document[s:e],
            start=s,
            end=e,
            index=i,
            heading_path=_heading_path_at(document, s),
        )
        for i, (s, e) in enumerate(spans)
    ]
