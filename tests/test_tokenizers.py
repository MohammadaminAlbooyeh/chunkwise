"""Custom tokenizer contract tests.

The only requirement on a tokenizer is that it's a callable from str to int,
monotonic in string length. These tests check chunkwise honors whatever
tokenizer it's given rather than assuming a characters-to-tokens ratio.
"""

from __future__ import annotations

from chunkwise import chunk


def word_count_tokenizer(text: str) -> int:
    return len(text.split())


def test_default_tokenizer_counts_characters() -> None:
    document = "x" * 50
    chunks = chunk(document, strategy="fixed", max_tokens=10, overlap=0)
    assert all(len(c.text) <= 10 for c in chunks)


def test_custom_tokenizer_is_respected() -> None:
    document = " ".join(["word"] * 100)
    chunks = chunk(
        document,
        strategy="fixed",
        max_tokens=10,
        overlap=0,
        tokenizer=word_count_tokenizer,
    )
    for c in chunks:
        assert word_count_tokenizer(c.text) <= 10


def test_tokenizer_affects_chunk_count() -> None:
    document = " ".join(["word"] * 100)
    char_chunks = chunk(document, strategy="fixed", max_tokens=50, overlap=0)
    word_chunks = chunk(
        document, strategy="fixed", max_tokens=50, overlap=0, tokenizer=word_count_tokenizer
    )
    assert len(char_chunks) != len(word_chunks) or len(document) == 0
