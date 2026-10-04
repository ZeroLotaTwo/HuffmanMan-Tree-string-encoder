## How to Use

> **Note:** This program currently requires you to edit the Python file directly to use these functions.

### Huffman Encoding

To encode a file using the Huffman tree, use the `encodeString()` function and provide the path to the file you want to encode.

```python
encodeString(r"[Path]")
```

For example:

```python
encodeString(r"C:\Users\Example\Documents\test.txt")
```

The program will create a `.huff` file containing the encoded Huffman tree.

The `.huff` file will be created **in the same directory as the original file**.

**Your original file will not be deleted or modified.**

---

### XOR Encryption

The program also includes XOR encryption and decryption using the `bitWiseXorEncrypt` functionality.

To encrypt a file, use:

```python
encryptFile(r"[Path]")
```

To decrypt an encrypted file, use:

```python
decyptFile(r"[Path]")
```

For example:

```python
encryptFile(r"C:\Users\Example\Documents\test.txt")
```

Then, to decrypt the file:

```python
decyptFile(r"C:\Users\Example\Documents\test.txt")
```

The encryption and decryption functions work similarly to the Huffman encoder: provide the path to the file you want to process, and the program will handle the rest.

> **Important:** Make sure you use the correct file path and keep track of which files have been encrypted so you can decrypt them when needed.
