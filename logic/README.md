# Logic Module

This folder contains the compression algorithms used by the project.

## Purpose

The module converts text into compact representations using classic lossless encoding techniques.
Each algorithm exposes a simple `encode()` and `decode()` interface so it can be reused by the command-line app and the TCP demo.

## Available algorithms

### Huffman

- Builds a frequency-based binary tree.
- Produces variable-length codes, with shorter codes for more frequent characters.
- Best suited for text with repeated symbols.

### Golomb

- Encodes characters as integers using quotient/remainder logic.
- Uses unary prefix bits plus a binary suffix.
- Requires `k` to be a power of two in this implementation.

### Elias-Gamma

- Encodes positive integers using unary length prefixing.
- Useful for compact integer representation.
- Accepts non-zero values only.

### Fibonacci

- Represents values using Fibonacci numbers.
- Produces a prefix-free code with a terminal `11` marker.
- Useful as a study example of alternative universal coding.

## Files

- `huffman.py` Huffman coding
- `golomb.py` Golomb coding
- `elias_gamma.py` Elias-Gamma coding
- `fibonacci.py` Fibonacci coding
- `assistance/node.py` helper node used by Huffman trees

## Typical usage

```python
from logic.huffman import Huffman

encoded = Huffman.encode("banana")
decoded = Huffman.decode(encoded)
```

## Notes

- Methods expect valid input for their algorithm.
- Some encoders work with text, while decoders may require binary strings in the expected format.
- The module is designed to stay simple and readable for educational use.
