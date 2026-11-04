"""Internal offset arithmetic shared by strategies.

Strategies operate on (start, end) integer spans, not strings, until the
final materialization step. This is what makes the offset invariant
structurally impossible to break.
"""

from __future__ import annotations

from .types import Chunk, Tokenizer

def _char_count(text: str) -> int:
    return len(text)


DEFAULT_TOKENIZER: Tokenizer = _char_count


def materialize(document: str, spans: list[tuple[int, int]]) -> list[Chunk]:
    """Turn (start, end) spans into Chunk objects with text sliced from document."""
    return [
        Chunk(text=document[start:end], start=start, end=end, index=i)
        for i, (start, end) in enumerate(spans)
    ]


def find_boundary(
    document: str,
    start: int,
    budget: int,
    tokenizer: Tokenizer,
) -> int:
    """Binary search for the largest end offset such that tokenizer(document[start:end]) <= budget.

    Works with any opaque tokenizer rather than assuming a fixed characters-to-tokens ratio.
    """
    lo, hi = start, len(document)
    if tokenizer(document[start:hi]) <= budget:
        return hi

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if tokenizer(document[start:mid]) <= budget:
            lo = mid
        else:
            hi = mid
    return lo if lo > start else min(start + 1, len(document))
