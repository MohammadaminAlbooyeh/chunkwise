"""Code-aware strategy: splits on function and class boundaries.

Planned for v0.2. Will use `ast` for Python and `tree-sitter` for other
languages to find boundaries, then chunk on those spans the same way
`recursive` chunks on separators.
"""

from __future__ import annotations

from ..types import Chunk, Tokenizer


def chunk_code(
    document: str,
    max_tokens: int,
    overlap: int,
    tokenizer: Tokenizer,
) -> list[Chunk]:
    raise NotImplementedError("chunk_code is planned for v0.2")
