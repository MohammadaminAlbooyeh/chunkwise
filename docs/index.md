# chunkwise

Text chunking for RAG with reversible offsets — every chunk is an exact slice of the source document.

## Why chunkwise

Most chunking libraries hand back a `list[str]`. The moment the text is detached from its origin, you can't highlight the passage a retrieval hit came from, expand a result to show surrounding context, or tell which section a passage lived under.

chunkwise holds one invariant across every strategy and every input:

```python
document[chunk.start:chunk.end] == chunk.text
```

## Quickstart

```python
from chunkwise import chunk

document = open("report.md").read()
chunks = chunk(document, strategy="markdown", max_tokens=512)

for c in chunks:
    assert document[c.start:c.end] == c.text
    print(c.heading_path, len(c.text))
```

## Contents

- [Strategies](strategies.md) — fixed, recursive, markdown, and what's planned
- [Tokenizers](tokenizers.md) — bringing your own token counter
- [Design](design.md) — why spans, not strings
