"""Hypothesis property tests for the core offset invariant.

The invariant: document[chunk.start:chunk.end] == chunk.text, for every
chunk, from every strategy, on every input.
"""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from chunkwise import chunk

STRATEGIES = ["fixed", "recursive", "markdown"]


@given(
    document=st.text(min_size=0, max_size=500),
    strategy=st.sampled_from(STRATEGIES),
    max_tokens=st.integers(min_value=1, max_value=200),
)
def test_offset_invariant_holds(document: str, strategy: str, max_tokens: int) -> None:
    chunks = chunk(document, strategy=strategy, max_tokens=max_tokens, overlap=0)
    for c in chunks:
        assert document[c.start : c.end] == c.text


@given(
    document=st.text(min_size=1, max_size=500),
    max_tokens=st.integers(min_value=1, max_value=200),
)
def test_non_overlapping_chunks_reconstruct_source(document: str, max_tokens: int) -> None:
    chunks = chunk(document, strategy="fixed", max_tokens=max_tokens, overlap=0)
    reconstructed = "".join(c.text for c in chunks)
    assert reconstructed == document


@given(
    document=st.text(min_size=0, max_size=300),
    max_tokens=st.integers(min_value=1, max_value=100),
)
def test_chunks_are_never_empty_except_for_empty_document(
    document: str, max_tokens: int
) -> None:
    chunks = chunk(document, strategy="recursive", max_tokens=max_tokens, overlap=0)
    if document == "":
        assert chunks == []
    else:
        assert all(len(c.text) > 0 for c in chunks)
