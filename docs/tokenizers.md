# Tokenizers

Token budgets depend on which model you're embedding for, so chunkwise doesn't hard-code one.

The `tokenizer` parameter accepts any callable from `str` to `int`:

```python
class Tokenizer(Protocol):
    def __call__(self, text: str) -> int: ...
```

## Default

The default counts characters, keeping the base install at zero dependencies:

```python
DEFAULT_TOKENIZER = len
```

## Bring your own

Pass a real token counter when you need accurate budgets for a specific model.

### tiktoken

```python
import tiktoken
from chunkwise import chunk

enc = tiktoken.get_encoding("cl100k_base")
chunks = chunk(document, max_tokens=512, tokenizer=lambda text: len(enc.encode(text)))
```

### transformers

```python
from transformers import AutoTokenizer
from chunkwise import chunk

tok = AutoTokenizer.from_pretrained("bert-base-uncased")
chunks = chunk(document, max_tokens=512, tokenizer=lambda text: len(tok.encode(text)))
```

## The only requirement

The token count must be monotonic in string length — a longer string never produces fewer tokens. Every real tokenizer satisfies this, and it's what lets chunkwise find chunk boundaries with binary search instead of assuming a fixed characters-to-tokens ratio.
