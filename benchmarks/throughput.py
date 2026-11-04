"""Throughput benchmark: chunkwise strategies vs. a naive splitter.

Run with: python benchmarks/throughput.py
"""

from __future__ import annotations

import time
from collections.abc import Callable

from chunkwise import chunk

SAMPLE_SIZE_CHARS = 200_000


def naive_split(document: str, max_tokens: int) -> list[str]:
    return [document[i : i + max_tokens] for i in range(0, len(document), max_tokens)]


def make_sample() -> str:
    paragraph = (
        "This is a benchmark paragraph used to measure chunking throughput. "
        "It repeats to simulate a long document.\n\n"
    )
    return paragraph * (SAMPLE_SIZE_CHARS // len(paragraph) + 1)


def time_it(label: str, fn: Callable[[], object]) -> None:
    start = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - start
    count = len(result) if isinstance(result, list) else -1
    print(f"{label:24s} {elapsed*1000:8.2f} ms  ({count} chunks)")


def main() -> None:
    document = make_sample()
    print(f"document size: {len(document):,} chars\n")

    time_it("naive_split", lambda: naive_split(document, 512))
    time_it("chunkwise fixed", lambda: chunk(document, strategy="fixed", max_tokens=512))
    time_it("chunkwise recursive", lambda: chunk(document, strategy="recursive", max_tokens=512))
    time_it("chunkwise markdown", lambda: chunk(document, strategy="markdown", max_tokens=512))


if __name__ == "__main__":
    main()
