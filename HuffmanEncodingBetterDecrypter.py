# from Queue import Queue
import heapq
from time import sleep, time
from typing import Final, Optional
from math import ceil

# this will be the longest code that will be saved. If you need longer you can change this number but it could brick other files and you'll need to change this number to what other file used.
longestBitString: Final = 16
# don't change these constants they just to maybe make it more reqdable
charIdx: Final = 0
numIdx: Final = 1
def countCharacters(string: str) -> list:
    global numIdx
    """Returns a list of tuples with (character, count)"""
    counter: dict = {}
    for char in string:
        counter[char] = counter.setdefault(char, 0) + 1
    newCounter = []
    for _ in range(len(counter)):
        newCounter.append(counter.popitem())
    return sorted(newCounter, key = lambda obj: obj[numIdx], reverse = True)

class CharNode:
    """
    This Node Structure is purely for the character with their frequency tuple
    I made another node class, because this would use less overall space than
    having the normal node just have a char variable being 0.
    """
    def __init__(self, character: str, frequency: int):
        self.frequency = frequency
        self.character = character
        # these are here so I know I hit a CharNode and the code relies on these being None
        self.left: None = None
        self.right: None = None

class Node:
    """
    These are nodes used for the huffman tree, but the ending nodes will have CharNodes.
    You can tell you hit a CharNode when you hit because when you hit None the CharNode will
    be above it.
    """
    def __init__(self):
        self.frequncySum: int = 0
        # these arn't typed because they hold to different types of nodes
        self.left: Optional[Node] | Optional[CharNode] = None
        self.right: Optional[Node] | Optional[CharNode] = None

    def __lt__(self, other):
        return self.frequncySum < other.frequncySum

class HuffmanTree:
    def __init__(self, string: str):
        global charIdx, numIdx
        if len(string) == 0:
            return
        frequencyArray: list[tuple[str, int]] = countCharacters(string)
        pq: list[Node] = []
        # This section empties the list to turn it into Nodes into the Queue
        node: Node = Node()
        oldLen = len(frequencyArray)
        for i in range(len(frequencyArray)):
            tupleObj: tuple[str, int] = frequencyArray.pop()
            if i % 2 == 0:
                node.left = CharNode(tupleObj[charIdx], tupleObj[numIdx])
                node.frequncySum += tupleObj[numIdx]
            elif i % 2:
                # works on the node pointer, but the node is in the Queue
                node.right = CharNode(tupleObj[charIdx], tupleObj[numIdx])
                node.frequncySum += tupleObj[numIdx]
                heapq.heappush(pq, node)
                node = Node()
        # if odd then it the last node will not be in the heap
        if oldLen % 2:
            heapq.heappush(pq, node)

        # this section now works in the Queue combining the nodes into a Huffman tree
        while len(pq) >= 2:
            newNode: Node = Node()
            newNode.left = heapq.heappop(pq)
            newNode.right = heapq.heappop(pq)
            newNode.frequncySum = newNode.left.frequncySum + newNode.right.frequncySum
            heapq.heappush(pq, newNode)
        self.Tree = heapq.heappop(pq)

    def createHuffmanCodeTable(self) -> dict[str, str]:
        """Returns a map where the character is the key and the value is the huffman code for the character."""
        huffmanCode: dict[str, str] = {}
        # How this visiting sytem works is
        # 0 means it has not visited left or right nodes
        # 1 means it has visited the left node but not right
        # 2 means it has visited both left and right and should be gone
        class visitNode:
            def __init__(self, node: Node | CharNode, visited: int):
                self.node: Node | CharNode = node
                self.visited: int = visited

        nodeStack: list[visitNode] = [visitNode(self.Tree, 0)]
        # 0 == went left. 1 == went right.
        currPath = []
        while nodeStack:
            currNode: Node | CharNode = nodeStack[-1].node
            visitingNum: int = nodeStack[-1].visited
            if visitingNum == 0:
                nodeStack[-1].visited += 1
                if currNode.left:
                    nodeStack.append(visitNode(currNode.left, 0))
                    currPath.append("0")
            elif visitingNum == 1:
                nodeStack[-1].visited += 1
                if currNode.right:
                    nodeStack.append(visitNode(currNode.right, 0))
                    currPath.append("1")
            elif visitingNum == 2:
                # If both of the nodes have nothing then it has to be a CharNode
                if currNode.left == None and currNode.right == None:
                    huffmanCode[currNode.character] = "".join(currPath) # type: ignore
                nodeStack.pop()
                if len(currPath):
                    currPath.pop()
        return huffmanCode

    def createCanonicalCodeTable(self) -> dict[str, str]:
        def getOrderedHuffmanCode(table: dict) -> list[tuple[str, str]]:
            """Insainly messy helper function to sort the codes by code length then by ascii value"""
            lenOrdered: list[tuple[str, str]] =  [table.popitem() for _ in range(len(table.keys()))]
            charIdx = 0
            codeIdx = 1
            # I will put in my own merge sort because insertion is probably pretty stupid if there are a lot of different codes.
            # def compareLenAndChar(a: tuple[str, str], b: tuple[str, str]) -> int:
            #     if len(a[codeIdx]) < len(b[codeIdx]):
            #         return -1
            #     elif len(a[codeIdx]) > len(b[codeIdx]):
            #         return 1
            #     else:
            #         if ord(a[charIdx]) < ord(b[charIdx]):
            #             return -1
            #         elif ord(a[charIdx]) > ord(b[charIdx]):
            #             return 1
            #         else:
            #             return 0
            lenOrdered = sorted(lenOrdered, key = lambda a: len(a[codeIdx]), )
            # insertion sort to finish this up, because I'm only sorting small sections by ascii value.
            for i in range(1, len(lenOrdered)):
                cmprIdx = i
                while(cmprIdx >= 1 and len(lenOrdered[cmprIdx][codeIdx]) == len(lenOrdered[cmprIdx - 1][codeIdx]) and ord(lenOrdered[cmprIdx][charIdx]) < ord(lenOrdered[cmprIdx - 1][charIdx])):
                    temp = lenOrdered[cmprIdx]
                    lenOrdered[cmprIdx] = lenOrdered[cmprIdx - 1]
                    lenOrdered[cmprIdx - 1] = temp
                    # print("nums", int(table[lenOrdered[cmprIdx][::-1]], 2), int(table[lenOrdered[cmprIdx - 1][::-1]], 2))
                    cmprIdx -= 1
            #     print("testing,",i, len(table[lenOrdered[cmprIdx]]), len(table[lenOrdered[cmprIdx - 1]]), (lenOrdered[cmprIdx]), (lenOrdered[cmprIdx - 1]))
            # for sym in lenOrdered:
            #     print(table[sym])
            return lenOrdered

        def add1(num: list[int]) -> None:
            carry = 1
            idx = len(num) - 1
            while carry and idx >=0:
                num[idx] += carry
                if num[idx] == 2:
                    num[idx] = 0
                    carry = 1
                else:
                    carry = 0
                idx -= 1

        sortedTable = getOrderedHuffmanCode(self.createHuffmanCodeTable())
        canonicalCode: dict[str, str] = {}
        createCode = []
        for tup in sortedTable:
            while len(createCode) < len(tup[numIdx]):
                createCode.append(0)
            canonicalCode[tup[charIdx]] = "".join([str(bit) for bit in createCode])
            # print(tup[charIdx], "".join([str(bit) for bit in createCode]))
            add1(createCode)
        return canonicalCode

def sendByte(fp, num: int):
    """Not completly sure how this method works tbh"""
    #print("num to byte,", int.to_bytes(num))
    fp.write(int.to_bytes(num))


def encodeString(fileName: str, string: str) -> None:
    """This will Encode the String and return the compressed string using canonical Huffman Encoding only supports ASCII characters. I fucked this up wanting it to be like how JPEG does it so now it's limited to ASCII I or no symbols that require more than 1 byte.
    """
    def getCodeLengths(table: dict) -> list[int]:
        # longestBitString = len(max(table.values(), key = lambda value: len(value)))
        # decided to hardcode number because in the jpeg format it decided to use 16 for this constant
        # because it would be more anyoing for decoding to have to know this and it probably better as constant
        global longestBitString
        codeLengths = [0 for i in range(longestBitString)]
        for value in table.values():
            codeLengths[len(value) - 1] += 1
        return codeLengths

    def getOrderedSymbols(table: dict) -> list[str]:
        """This is utilizing the feature that python has that in the dicts it is ordered on insertion of the items, and the symbols were inserted in order of code length then ascii value"""
        return [key for key in table.keys()]

    huffmanTree: HuffmanTree = HuffmanTree(string)
    huffmanTable: dict[str, str] = huffmanTree.createCanonicalCodeTable()
    codeLength: list[int] = getCodeLengths(huffmanTable)
    totalBytesLength: int = sum(codeLength) + len(codeLength) + 1
    with open(fileName + ".huff","w+b") as f:
        sendByte(f,totalBytesLength)
        for code in codeLength:
            sendByte(f,code)
        for symbol in getOrderedSymbols(huffmanTable):
        #    print(symbol, ord(symbol))
           sendByte(f,ord(symbol))
        bytesToSend = ""
        num = 0
        for char in string:
            bytesToSend += huffmanTable[char]
            # this if statement checks to see if it is ready to send a full byte, because you can't send a single bit
            while len(bytesToSend) >= 8:
                for bit in bytesToSend[:8]:
                    num <<= 1
                    num += int(bit)
                # print("Sending Byte", num)
                # sleep(1)
                sendByte(f, num)
                bytesToSend = bytesToSend[8:]
                num = 0
        for bit in bytesToSend:
            num <<= 1
            num += int(bit)
        for _ in range(8 - len(bytesToSend)):
            num <<= 1
        # print(bytesToSend)
        # print(num)
        sendByte(f, num)
        # print(len(bytesToSend))
        sendByte(f, len(bytesToSend)) # how many valid bits are left

def decodeString(fileName):
    global longestBitString

    class decodeNode:
        def __init__(self):
            self.data: str = None #type: ignore
            self.left: decodeNode = None #type: ignore
            self.right: decodeNode = None #type: ignore

    def add1(num: list[int]) -> None:
        carry = 1
        idx = len(num) - 1
        while carry and idx >=0:
            num[idx] += carry
            if num[idx] == 2:
                num[idx] = 0
                carry = 1
            else:
                carry = 0
            idx -= 1

    with open(fileName, "r+b") as f:
        # reads the length of the Huffman Table section
        tableLen: int = int.from_bytes(f.read1(1),"big")
        codeLengths: list[int] = [int.from_bytes(f.read1(1),"big") for _ in range(longestBitString)]
        minCode: int = 0
        for i in range(len(codeLengths)):
            if codeLengths[i]:
                minCode = i + 1
                break
        symbols: list[str] = [chr(int.from_bytes(f.read1(1),"big")) for _ in range(tableLen - longestBitString - 1)]
        # creates a huffman tree for decoding
        root: decodeNode = decodeNode()
        curSymIdx: int = 0
        curCode: list[int] = []
        for i in range(len(codeLengths)):
            curCode.append(0)
            while codeLengths[i]:
                curNode: decodeNode = root
                for path in curCode:
                    if path == 0:
                        if not curNode.left:
                            curNode.left = decodeNode()
                        curNode = curNode.left
                    else: # path == 1
                        if not curNode.right:
                            curNode.right = decodeNode()
                        curNode = curNode.right
                curNode.data = symbols[curSymIdx]
                curNode = root
                add1(curCode)
                codeLengths[i] -= 1
                curSymIdx += 1

        def readNextBits(fp) -> str:
            """Reads from the file and returns a string of the bits that are either greater than the longestBitString or less if we reach then end of the file."""
            encyptedString: str = ""
            for _ in range(ceil(longestBitString / 8)):
                read: bytes = fp.read1(1)
                if not read:
                    return encyptedString
                num = int.from_bytes(read, "big")
                for i in range(8):
                    encyptedString += str((num >> (7 - i)) & 1)
            return encyptedString

        # this section actually starts reading the code and decodes it
        with open("Works_Prop" + ".txt", "w") as out:
            encyptedString: str = readNextBits(f) + readNextBits(f)
            toAppend: str = readNextBits(f)
            # toBreak = 0
            validBits = 0
            while encyptedString != "":
                rang = longestBitString
                if toAppend == "":
                    validBits = int(encyptedString[len(encyptedString) - 8:], 2)
                    encyptedString = encyptedString[:len(encyptedString) - 16 + validBits]
                    validBits = 8 - validBits
                    rang = len(encyptedString)
                for i in range(rang):
                    if encyptedString[i] == "0":
                        curNode = curNode.left
                        # print("Went Left")
                        if curNode == None:
                            print("There is something faulty with the file")
                            return
                    else:
                        curNode = curNode.right
                        # print("Went Right")
                        if curNode == None:
                            print("There is something faulty with the file")
                            return
                    if curNode.data:
                        #out.write(curNode.data)
                        print(curNode.data, end="")
                        curNode = root
                encyptedString = encyptedString[rang:] + toAppend
                #print(encyptedString)
                toAppend = readNextBits(f)
                #sleep(1)
                # toBreak += 1
                # if toBreak >= 2:
                #     return

# file = r"C:\Users\justi\Documents\Tank_Man.txt"
# file = r"C:\Users\justi\Downloads\swears.txt"
# file = r"C:\Users\justi\Downloads\large\bible.txt"
# file = r"C:\Users\justi\AppData\Local\Programs\Microsoft VS Code\ThisIsDecodeTest.txt"
file = r"C:\Users\justi\Documents\scratch.txt"
with open(file, "r") as f:
    string = f.read()

encodeString(r"C:\Users\justi\Documents\DOCS\8_30_2026", string)
# encodeString(r"C:\Users\justi\Downloads\scratch.huffff", string)
# decodeString(r"C:\Users\justi\Downloads\scratch.huffff")
#decodeString(r"C:\Users\justi\Documents\DOCS\8_19_2025.huff")
#r"C:\Users\justi\Documents\DOCS"
# start = time()
# decodeString(r"C:\Users\justi\AppData\Local\Programs\Microsoft VS Code\Encoded.huff")

# print("Done Encoding, took", time() - start)
