# Contributing

Thanks for considering a contribution to chunkwise.

## Setup

```bash
git clone https://github.com/amin-albooyeh/chunkwise.git
cd chunkwise
pip install -e ".[dev]"
```

## Running checks

```bash
ruff check .
mypy src/chunkwise
pytest
```

All three run in CI on every pull request, across Python 3.10–3.13.

## Guidelines

- The offset invariant (`document[chunk.start:chunk.end] == chunk.text`) must hold for every strategy on every input. Any new strategy needs a corresponding Hypothesis property test in `tests/test_invariants.py`.
- Strategies operate on `(start, end)` spans internally and only materialize text via `_spans.materialize`. Don't build chunks by slicing and reassembling strings inside a strategy.
- Keep the base install dependency-free. Anything that requires a third-party package (e.g. `semantic`) ships as an optional extra.
- Add tests for new behavior in `tests/test_strategies.py` or `tests/test_tokenizers.py` as appropriate.

## Reporting issues

Open a GitHub issue with a minimal reproducible example — ideally the document text, the strategy, and the parameters used.
