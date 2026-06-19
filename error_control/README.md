# Error Control Module

This folder contains the protection and validation techniques used after compression.

## Purpose

The module helps detect or correct transmission errors in encoded messages.
It is used mainly in the TCP demo, where data is compressed first and then protected before being sent.

## Available tools

### CRC

- Generates a checksum using polynomial division in binary.
- Useful for detecting transmission errors.
- The generator polynomial in this project is fixed to `10011`.

### Hamming

- Implements a Hamming(7,4) style code.
- Can detect and correct a single-bit error in each codeword.
- Works on binary strings and preserves leftover bits that do not fit a full block.

### Repetition

- Repeats each bit a chosen number of times.
- Decoding uses majority vote inside each block.
- Simple and easy to understand, though less efficient than CRC or Hamming.

### Error simulator

- Flips one bit at a chosen position.
- Can also flip multiple random bit positions.
- Used to emulate noisy transmission during tests.

## Files

- `crc.py` CRC generation and verification
- `hamming.py` Hamming encoding, error detection, and correction
- `repetition_ri.py` repetition-based protection
- `error.py` error simulation utilities

## Typical usage

```python
from error_control.crc import crc_generator

crc = crc_generator()
protected = crc.gerar_mensagem_crc("101100")
check = crc.verificar_crc(protected)
```

## Notes

- These utilities expect binary strings.
- CRC is best for detection, Hamming for correction, and repetition for simple redundancy-based protection.
- The module is intentionally straightforward so it can be studied and extended easily.
