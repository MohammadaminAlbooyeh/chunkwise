# Design notes: why spans, not strings

## The problem with returning strings

Most chunking libraries return `list[str]`. Once text is detached from its origin:

- You can't highlight the passage a retrieval hit came from in the original document.
- You can't expand a result to show the surrounding paragraph.
- You can't tell which section or heading a passage lived under.

Worse, splitters that strip or normalize whitespace silently drop characters — a failure mode that shows up only as retrieval quietly missing content, which is hard to notice and harder to debug.

## The guarantee

chunkwise holds one invariant across every strategy and every input:

```python
document[chunk.start:chunk.end] == chunk.text
```

This is enforced three ways:

1. **Structurally** — internal logic operates on `(start, end)` integer pairs ([`_spans.py`](../src/chunkwise/_spans.py)) and only materializes text at the final step. No strategy, present or future, can break the invariant even by accident.
2. **At runtime** — the `Chunk` type validates its own span on construction (see `Chunk.__post_init__` in [`types.py`](../src/chunkwise/types.py)).
3. **In CI** — a Hypothesis property test ([`test_invariants.py`](../tests/test_invariants.py)) runs against generated documents on every commit, alongside a test that concatenating non-overlapping chunks reproduces the source byte for byte.

## Consequences

These are deliberate, not accidental:

- Chunks are never stripped, normalized, or rewritten.
- Overlap widens a chunk backwards into real preceding text rather than gluing on a copied prefix.
- Window boundaries are found by binary search over character offsets (`find_boundary` in `_spans.py`), so the library works with any opaque tokenizer rather than assuming a fixed characters-to-tokens ratio.
