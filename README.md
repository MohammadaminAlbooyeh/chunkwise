# chunkwise

Text chunking for RAG with reversible offsets — every chunk is an exact slice of the source document.

chunkwise splits documents into embeddable chunks for retrieval-augmented generation. Unlike most splitters, which return detached strings, every chunk carries the exact character range it came from, so `document[chunk.start:chunk.end] == chunk.text` always holds — making source highlighting, citation, and context expansion possible. Zero dependencies, bring-your-own tokenizer, and structure-aware strategies for plain text and Markdown.

## Install

```bash
pip install chunkwise
```

## Usage

```python
from chunkwise import chunk

document = "..."
chunks = chunk(document, strategy="recursive", max_tokens=512, overlap=50)

for c in chunks:
    assert document[c.start:c.end] == c.text
```

## Strategies

| Strategy | Behavior |
|---|---|
| `fixed` | Hard windows of N tokens with configurable overlap. Fast, boundary-blind. Suited to logs and unstructured text. |
| `recursive` | Falls back through a separator chain — paragraphs, then lines, then sentences, then words — breaking on the coarsest boundary that fits the budget. The default. |
| `markdown` | Keeps fenced code blocks intact and tags every chunk with its heading path (e.g. `["Guide", "Install"]`), giving retrieval results a sense of place. |

Planned: `code` (v0.2, AST / tree-sitter boundaries) and `semantic` (v0.3, embedding similarity cuts), the latter shipping as an optional extra so the base install stays dependency-free.

## Tokenizer independence

Token budgets depend on which model you're embedding for, so chunkwise doesn't hard-code one. The `tokenizer` parameter accepts any callable from `str` to `int`. The default counts characters, keeping the base install at zero dependencies; pass a `tiktoken` or `transformers` counter when you need real token budgets.

## The guarantee

chunkwise holds one invariant across every strategy and every input:

```
document[chunk.start:chunk.end] == chunk.text
```

Enforced structurally (strategies operate on offsets, not strings), at runtime (`Chunk` validates its own span), and in CI (Hypothesis property tests on every commit). See [docs/design.md](docs/design.md) for the full rationale.

## Status

v0.1.0. Python 3.10+. MIT licensed. Zero runtime dependencies.

## Documentation

- [docs/index.md](docs/index.md)
- [docs/strategies.md](docs/strategies.md)
- [docs/tokenizers.md](docs/tokenizers.md)
- [docs/design.md](docs/design.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
