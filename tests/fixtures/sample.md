# Guide

Welcome to the guide. This section introduces the project.

## Install

Run the following command to install the package:

```bash
pip install chunkwise
```

That's all you need for the base install.

## Usage

```python
from chunkwise import chunk

chunks = chunk("some long document", strategy="markdown")
```

### Advanced

Heading paths let you tag each chunk with its place in the document, such
as `["Guide", "Usage", "Advanced"]`.
