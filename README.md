# chunkwise

**Text chunking for RAG with reversible offsets — every chunk is an exact slice of the source document.**

[![CI](https://github.com/amin-albooyeh/chunkwise/actions/workflows/ci.yml/badge.svg)](https://github.com/amin-albooyeh/chunkwise/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/chunkwise.svg)](https://pypi.org/project/chunkwise/)
[![Python versions](https://img.shields.io/pypi/pyversions/chunkwise.svg)](https://pypi.org/project/chunkwise/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

chunkwise splits documents into embeddable chunks for retrieval-augmented generation. Unlike most splitters, which return detached strings, every chunk carries the exact character range it came from, so `document[chunk.start:chunk.end] == chunk.text` always holds — making source highlighting, citation, and context expansion possible. Zero runtime dependencies, bring-your-own tokenizer, and structure-aware strategies for plain text and Markdown.

## Why chunkwise

Most chunking libraries hand back a `list[str]`. The moment text is detached from its origin, three things become impossible:

- You can't **highlight** the passage a retrieval hit came from in the original document.
- You can't **expand** a result to show the surrounding paragraph.
- You can't tell **which section or heading** a passage lived under.

Worse, splitters that strip or normalize whitespace silently drop characters — a failure mode that shows up only as retrieval quietly missing content, which is hard to notice and harder to debug.

## Install

```bash
pip install chunkwise
```

No dependencies are pulled in. (An optional `semantic` extra will be added in v0.3 for embedding-based chunking.)

## Quickstart

```python
from chunkwise import chunk

document = open("report.md").read()
chunks = chunk(document, strategy="recursive", max_tokens=512, overlap=50)

for c in chunks:
    assert document[c.start:c.end] == c.text  # always true, for every chunk
    print(c.index, c.start, c.end, c.heading_path)
```

## The guarantee

chunkwise holds one invariant across every strategy and every input:

```python
document[chunk.start:chunk.end] == chunk.text
```

This is enforced three ways:

1. **Structurally** — internal logic operates on `(start, end)` integer spans and only materializes text at the final step, so no strategy (present or future) can break the invariant even by accident.
2. **At runtime** — the `Chunk` type validates its own span on construction.
3. **In CI** — a Hypothesis property test runs against generated documents on every commit, alongside a test that concatenating non-overlapping chunks reproduces the source byte for byte.

The consequences are deliberate: chunks are never stripped, normalized, or rewritten, and overlap widens a chunk backwards into real preceding text rather than gluing on a copied prefix.

See [docs/design.md](docs/design.md) for the full rationale.

## Strategies

| Strategy | Behavior |
|---|---|
| `fixed` | Hard windows of N tokens with configurable overlap. Fast, boundary-blind. Suited to logs and unstructured text. |
| `recursive` | Falls back through a separator chain — paragraphs, then lines, then sentences, then words — breaking on the coarsest boundary that fits the budget. **The default.** |
| `markdown` | Keeps fenced code blocks intact and tags every chunk with its heading path (e.g. `["Guide", "Install"]`), giving retrieval results a sense of place. |

Planned: `code` (v0.2 — AST / tree-sitter boundaries) and `semantic` (v0.3 — embedding similarity cuts), the latter shipping as an optional extra so the base install stays dependency-free.

See [docs/strategies.md](docs/strategies.md) for guidance on choosing one.

## Tokenizer independence

Token budgets depend on which model you're embedding for, so chunkwise doesn't hard-code one. The `tokenizer` parameter accepts any callable from `str` to `int`:

```python
from chunkwise import chunk
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
chunks = chunk(document, max_tokens=512, tokenizer=lambda text: len(enc.encode(text)))
```

The default counts characters, keeping the base install at zero dependencies. The only requirement on a tokenizer is that its count is monotonic in string length — every real tokenizer satisfies this. See [docs/tokenizers.md](docs/tokenizers.md).

## API

```python
def chunk(
    document: str,
    strategy: str = "recursive",   # "fixed" | "recursive" | "markdown"
    max_tokens: int = 512,
    overlap: int = 0,
    tokenizer: Tokenizer = ...,    # str -> int, defaults to len
) -> list[Chunk]: ...
```

Each `Chunk` is a frozen dataclass:

```python
@dataclass(frozen=True, slots=True)
class Chunk:
    text: str
    start: int
    end: int
    index: int
    heading_path: tuple[str, ...]  # populated by the markdown strategy
```

## Status

v0.1.0 · Python 3.10+ · MIT licensed · zero runtime dependencies · tested on CI across Python 3.10–3.13.

## Documentation

- [docs/index.md](docs/index.md) — overview and quickstart
- [docs/strategies.md](docs/strategies.md) — strategy reference and how to choose
- [docs/tokenizers.md](docs/tokenizers.md) — bringing your own tokenizer
- [docs/design.md](docs/design.md) — why spans, not strings

## Benchmarks

```bash
python benchmarks/throughput.py
```

Compares chunkwise strategies against a naive fixed-width splitter on a synthetic document.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for setup, checks, and guidelines (in particular, the offset invariant that any new strategy must preserve).

## License

MIT — see [LICENSE](LICENSE).
