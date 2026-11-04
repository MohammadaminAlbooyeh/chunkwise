"""Core types: the Chunk dataclass and the Tokenizer protocol."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@runtime_checkable
class Tokenizer(Protocol):
    """Any callable from str to an integer token count.

    The only requirement is that the count is monotonic in string length —
    every real tokenizer (character counting, tiktoken, transformers) satisfies this.
    """

    def __call__(self, text: str) -> int: ...


@dataclass(frozen=True, slots=True)
class Chunk:
    """A chunk of a source document.

    The invariant ``document[chunk.start:chunk.end] == chunk.text`` is enforced
    on construction: a Chunk cannot exist with a span that doesn't match its text.
    """

    text: str
    start: int
    end: int
    index: int = 0
    heading_path: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.end - self.start != len(self.text):
            raise ValueError(
                f"Chunk span ({self.start}, {self.end}) does not match "
                f"text length {len(self.text)}"
            )
        if self.start < 0 or self.end < self.start:
            raise ValueError(f"Invalid span: ({self.start}, {self.end})")
