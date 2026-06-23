# Compression and Error Control

This educational Python project was developed in two parts. It explores lossless data compression and then extends the same algorithms into a client/server application that simulates transmission errors and applies error-control techniques.

## Overview

### Part 1 — Data compression

The first part implements Elias-Gamma, Fibonacci, Golomb, and Huffman coding in `logic/`. The Huffman algorithm uses the helper node in `logic/assistance/node.py`, while `main.py` provides an interactive terminal interface for encoding and decoding data locally.

### Part 2 — Transmission and error control

The second part reuses the compression algorithms in a TCP client/server system. `client.py` collects the user's choices, `auxiliar.py` builds the menus and coordinates the selected methods, and `server.py` processes each request. The `error_control/` package adds CRC, Hamming code, repetition coding, and error simulation so encoded messages can be protected and tested during transmission.

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
|   |-- assistance/
|   |   `-- node.py
|   |-- elias_gamma.py
|   |-- fibonacci.py
|   |-- golomb.py
|   `-- huffman.py
`-- error_control/
    |-- crc.py
    |-- error.py
    |-- hamming.py
    `-- repetition_ri.py
```

For more detail, see [logic/README.md](logic/README.md) and [error_control/README.md](error_control/README.md).

## Notes

- Compression algorithms work on text or binary representations depending on the method.
- Error control is applied after compression in the network flow.
- The project is intended for study, demonstrations, and algorithm comparison.
