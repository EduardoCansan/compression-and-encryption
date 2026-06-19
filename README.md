# Compression and Cryptography

This project is a small Python study base for data compression and basic error control.
It includes classic encoding algorithms, message protection techniques, and a simple TCP client/server flow for end-to-end testing.

## Overview

- `logic/` contains the compression algorithms.
- `error_control/` contains the error detection and correction utilities.
- `main.py` provides a local terminal menu for encode/decode tests.
- `server.py` and `client.py` demonstrate a networked flow that combines compression and error control.

## Features

- Huffman coding
- Golomb coding
- Elias-Gamma coding
- Fibonacci coding
- CRC-based error detection
- Hamming-based error correction
- Repetition-based protection
- Bit error simulation

## Requirements

The project uses the `rich` library for improved terminal output.

```bash
pip install rich
```

## How to run

Local menu:

```bash
python main.py
```

TCP demo:

```bash
python server.py
python client.py
```

## Project structure

```text
.
|-- main.py
|-- client.py
|-- server.py
|-- auxiliar.py
|-- logic/
|   `-- README.md
`-- error_control/
    `-- README.md
```

For more detail, see [logic/README.md](logic/README.md) and [error_control/README.md](error_control/README.md).

## Notes

- Compression algorithms work on text or binary representations depending on the method.
- Error control is applied after compression in the network flow.
- The project is intended for study, demonstrations, and algorithm comparison.
