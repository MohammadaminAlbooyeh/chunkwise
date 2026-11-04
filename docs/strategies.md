# Strategies

| Strategy | Behavior |
|---|---|
| `fixed` | Hard windows of N tokens with configurable overlap. Fast, boundary-blind. Suited to logs and unstructured text. |
| `recursive` | Falls back through a separator chain — paragraphs, then lines, then sentences, then words — breaking on the coarsest boundary that fits the budget. The default. |
| `markdown` | Keeps fenced code blocks intact and tags every chunk with its heading path (e.g. `["Guide", "Install"]`), giving retrieval results a sense of place. |

## Planned

- `code` (v0.2) — splits on function and class boundaries via `ast` and `tree-sitter`.
- `semantic` (v0.3) — cuts where sentence-embedding similarity drops. Ships as an optional extra (`pip install chunkwise[semantic]`) so the base install stays dependency-free.

## Choosing a strategy

- Use `fixed` when the input has no structure to exploit (logs, transcripts) or when you need predictable, uniform chunk sizes.
- Use `recursive` as the default for prose and general text.
- Use `markdown` for documentation, READMEs, or any Markdown source where heading context and code fences matter.

## Common parameters

Every strategy takes the same three parameters:

- `max_tokens` — the token budget per chunk, as measured by the tokenizer.
- `overlap` — how many tokens of overlap between consecutive chunks. Overlap widens a chunk backwards into real preceding text; it never duplicates a copied prefix.
- `tokenizer` — see [tokenizers.md](tokenizers.md).
