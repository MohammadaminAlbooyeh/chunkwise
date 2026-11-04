"""chunkwise: text chunking for RAG with reversible offsets.

Every chunk carries the exact character range it came from, so
``document[chunk.start:chunk.end] == chunk.text`` always holds.
"""

from __future__ import annotations

from ._spans import DEFAULT_TOKENIZER
from .strategies import chunk_fixed, chunk_markdown, chunk_recursive
from .types import Chunk, Tokenizer

__version__ = "0.1.0"

_STRATEGIES = {
    "fixed": chunk_fixed,
    "recursive": chunk_recursive,
    "markdown": chunk_markdown,
}


def chunk(
    document: str,
    strategy: str = "recursive",
    max_tokens: int = 512,
    overlap: int = 0,
    tokenizer: Tokenizer = DEFAULT_TOKENIZER,
) -> list[Chunk]:
    """Split `document` into a list of Chunk objects.

    Args:
        document: the source text to split.
        strategy: one of "fixed", "recursive" (default), "markdown".
        max_tokens: the token budget per chunk, as measured by `tokenizer`.
        overlap: how many tokens of overlap between consecutive chunks.
        tokenizer: a callable from str to int token count. Defaults to
            character counting, keeping the base install dependency-free.
    """
    try:
        strategy_fn = _STRATEGIES[strategy]
    except KeyError:
        raise ValueError(
            f"Unknown strategy {strategy!r}. Available: {sorted(_STRATEGIES)}"
        ) from None
    return strategy_fn(document, max_tokens, overlap, tokenizer)


__all__ = ["chunk", "Chunk", "Tokenizer", "__version__"]
