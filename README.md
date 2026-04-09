# 📦 Compression and 🔐 Cryptography

## **Integrantes do Grupo:** Gustavo Mezomo, Pedro Gustavo Thomas, Eduardo Cansan

This repository introduces fundamental concepts of **Data Compression** and **Cryptography**, along with Python implementations of classic encoding and decoding techniques.

The goal is to provide a simple theoretical foundation before exploring the implemented code.

---

## 📚 What is Compression?

**Data compression** is the process of reducing the size of data to save storage space or speed up transmission.

It can be:

* **Lossless:** allows exact reconstruction of the original data
* **Lossy:** loses some information (e.g., JPEG images)

In this project, we focus on **lossless compression** methods.

---

## 🔐 What is Cryptography?

**Cryptography** is used to protect information, making it unreadable to unauthorized users.

Main difference:

* **Compression → efficiency**
* **Cryptography → security**

Both involve transforming data, but for different purposes.

---

# 🧠 Encoding Techniques

Below are the main methods implemented in this project:

---

## 🔢 Golomb Coding

### 📌 What is it

**Golomb Coding** is used to compress integers and is especially efficient when data follows a **geometric distribution**.

### ⚙️ How it works

* Choose a parameter `m`
* A number `n` is divided into:

  * **Quotient (q)** → encoded in **unary**
  * **Remainder (r)** → encoded in **truncated binary**

### 🔄 Decoding

* Read unary value → get `q`
* Read remaining bits → get `r`
* Reconstruct:

  ```
  n = q * m + r
  ```

### 💡 Use case

* Data with many small values

---

## 📈 Elias-Gamma Coding

### 📌 What is it

**Elias-Gamma Coding** is a universal method for encoding positive integers.

### ⚙️ How it works

For a number `n`:

1. Write `n` in binary
2. Count the number of bits (`k`)
3. Add `k-1` leading zeros

### Example:

```
n = 10 → binary: 1010
k = 4 → prefix: 000
Result: 0001010
```

### 🔄 Decoding

* Count leading zeros → determine length
* Read the remaining bits
* Reconstruct the number

### 💡 Advantage

* Simple and efficient for small numbers

---

## 🧮 Fibonacci Coding

### 📌 What is it

Uses the Fibonacci sequence to uniquely represent integers.

### ⚙️ How it works

* Decompose the number into a sum of Fibonacci numbers (no consecutive ones)
* Represent using bits (1 = used, 0 = not used)
* End with **"11"** as a delimiter

### Example:

```
n = 10 → 8 + 2
Representation: 01001011
```

### 🔄 Decoding

* Read until "11" is found
* Reconstruct by summing Fibonacci values

### 💡 Key feature

* Prefix-free code (no ambiguity)

---

## 🌳 Huffman Coding

### 📌 What is it

**Huffman Coding** is one of the most important lossless compression algorithms.

### ⚙️ How it works

1. Count symbol frequencies
2. Build a **binary tree**
3. More frequent symbols get shorter codes

### Example:

```
A: 50% → 0
B: 25% → 10
C: 15% → 110
D: 10% → 111
```

### 🔄 Decoding

* Traverse the tree:

  * 0 → left
  * 1 → right
* When reaching a leaf → symbol found

### 💡 Advantage

* Efficient compression based on real data frequency

---

# 🧾 Summary

| Method      | Data Type | Complexity | Highlight                        |
| ----------- | --------- | ---------- | -------------------------------- |
| Golomb      | Integers  | Medium     | Great for specific distributions |
| Elias-Gamma | Integers  | Low        | Simple and universal             |
| Fibonacci   | Integers  | Medium     | Unique representation            |
| Huffman     | Symbols   | Medium     | Frequency-based compression      |

---

# 🚀 Project Goal

This repository aims to:

* Demonstrate fundamental compression concepts
* Implement classical algorithms in Python
* Serve as a study base for:

  * Information Theory
  * Data Structures
  * Data Processing