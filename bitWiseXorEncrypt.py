from typing import Generator

def key() -> Generator:
    first = 0
    second = 1
    while True:
        ret = (first + second) % 256
        yield ret
        first, second = second, ret


def bitwiseEncrypt(byte: bytes, gen: Generator) -> bytes:
    return int.to_bytes((int.from_bytes(byte, "big") ^ next(gen)))

def encyptFile(fileName: str) -> None:
    gen = key()
    with open(fileName, "rb") as r, open(f"{fileName.split('.')[0]}.cust", "wb") as w:
        byte = r.read1(1)
        #print(byte, int.from_bytes(byte, "big"))
        while byte:
            w.write(bitwiseEncrypt(byte, gen))
            byte = r.read1(1
                           )
def decyptFile(fileName: str) -> None:
    gen = key()
    with open(fileName, "rb") as r, open(f"{fileName.split('.')[0]}.huff", "wb") as w:
        byte = r.read1(1)
        #print(byte, int.from_bytes(byte, "big"))
        while byte:
            w.write(bitwiseEncrypt(byte, gen))
            byte = r.read1(1)

# fileName = r"C:\Users\justi\Downloads\5_05_2026"
fileName = r"C:\Users\justi\Documents\DOCS\8_30_2026.huff"
encyptFile(fileName)
# decyptFile(fileName)