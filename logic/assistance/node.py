# Normal Node class for huffman tree
# Add frequency and character to the node, for validation
class Node:
    def __init__(self, char, freq):
        self.char  = char   
        self.freq  = freq
        self.left  = None 
        self.right = None


# OBS: The lt is a magic method in python that is used to compare two objects 
#      using the < operator. In this case, it compares the frequency of two nodes, 
#      which is essential for building the Huffman tree using a priority queue (min-heap).
    def __lt__(self, other):
        return self.freq < other.freq