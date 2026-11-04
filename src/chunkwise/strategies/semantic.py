"""Semantic strategy: cuts where sentence-embedding similarity drops.

Planned for v0.3, shipping as an optional extra (`pip install chunkwise[semantic]`)
so the base install stays dependency-free.
"""

from __future__ import annotations

from ..types import Chunk, Tokenizer


def chunk_semantic(
    document: str,
    max_tokens: int,
    overlap: int,
    tokenizer: Tokenizer,
) -> list[Chunk]:
    raise NotImplementedError(
        "chunk_semantic is planned for v0.3 and requires the 'semantic' extra"
    )
