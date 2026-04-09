import heapq
from collections import Counter
from logic.assistance.node import Node

class Huffman:

    @staticmethod
    def encode(text: str) -> str:
        root, table = Huffman._build_tree(text)

        bits = "".join(table[c] for c in text)

        # Store the table alongside bits so decode can work standalone
        # Format: "a:0,b:10,n:11|100110110"
        table_str = ",".join(f"{c}:{code}" for c, code in table.items())
        return f"{table_str}|{bits}"

    @staticmethod
    def decode(encoded: str) -> str:
        if "|" not in encoded:
            raise ValueError("Invalid Huffman string. Expected format: table|bits")

        table_str, bits = encoded.split("|", 1)

        # Rebuild reverse table: code → char
        reverse_table = {}
        for entry in table_str.split(","):
            char, code = entry.split(":", 1)
            reverse_table[code] = char

        # Decode by matching prefixes
        result = []
        buffer = ""
        for bit in bits:
            buffer += bit
            if buffer in reverse_table:
                result.append(reverse_table[buffer])
                buffer = ""

        if buffer:
            raise ValueError(f"Leftover bits could not be decoded: {buffer}")

        return "".join(result)

    @staticmethod
    def _build_tree(text: str):
        freq = Counter(text)
        heap = [Node(char, f) for char, f in freq.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left  = heapq.heappop(heap)
            right = heapq.heappop(heap)

            parent       = Node(None, left.freq + right.freq)
            parent.left  = left
            parent.right = right

            heapq.heappush(heap, parent)

        root  = heap[0]
        table = Huffman._generate_codes(root)
        return root, table

    @staticmethod
    def _generate_codes(node, prefix="", table=None):
        if table is None:
            table = {}

        if node.char is not None:
            table[node.char] = prefix or "0"
        else:
            Huffman._generate_codes(node.left,  prefix + "0", table)
            Huffman._generate_codes(node.right, prefix + "1", table)

        return table