# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-11-04

### Added

- Initial release.
- `chunk()` public API with `fixed`, `recursive`, and `markdown` strategies.
- `Chunk` dataclass enforcing `document[chunk.start:chunk.end] == chunk.text`.
- Tokenizer protocol with a character-counting default; zero runtime dependencies.
- Hypothesis-based property tests for the offset invariant.
