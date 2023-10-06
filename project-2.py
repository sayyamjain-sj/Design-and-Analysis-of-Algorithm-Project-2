import time
import heapq
from collections import defaultdict
import matplotlib.pyplot as plt

class Node:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def calculate_frequency(input_symbols):
    frequency = defaultdict(int)
    for symbol in input_symbols:
        frequency[symbol] += 1
    return frequency

def build_huffman_tree(frequency):
    heap = [Node(symbol, freq) for symbol, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left_child = heapq.heappop(heap)
        right_child = heapq.heappop(heap)

        internal_node = Node(frequency=None)
        internal_node.frequency = left_child.frequency + right_child.frequency
        internal_node.left = left_child
        internal_node.right = right_child

        heapq.heappush(heap, internal_node)

    return heap[0]  # Return the root of the Huffman tree

def generate_huffman_codes(node, current_code, codes):
    if node.symbol:
        codes[node.symbol] = current_code
        return

    generate_huffman_codes(node.left, current_code + '0', codes)
    generate_huffman_codes(node.right, current_code + '1', codes)

def huffman_encoding(input_symbols):
    frequency = calculate_frequency(input_symbols)
    root = build_huffman_tree(frequency)
    codes = {}
    generate_huffman_codes(root, '', codes)

    encoded_text = ''.join(codes[symbol] for symbol in input_symbols)
    return encoded_text, codes

def huffman_decoding(encoded_text, codes):
    reversed_codes = {code: symbol for symbol, code in codes.items()}
    current_code = ''
    decoded_symbols = []

    for bit in encoded_text:
        current_code += bit
        if current_code in reversed_codes:
            decoded_symbols.append(reversed_codes[current_code])
            current_code = ''

    return ''.join(decoded_symbols)

def measure_time_complexity(input_sizes):
    time_complexity = []
    
    for size in input_sizes:
        input_symbols = ['A'] * size  # For simplicity, we use the same symbol repeatedly
        start_time = time.time()
        encoded_text, _ = huffman_encoding(input_symbols)
        end_time = time.time()
        time_complexity.append(end_time - start_time)
    
    return time_complexity

def plot_time_complexity(input_sizes, time_complexity):
    plt.plot(input_sizes, time_complexity, marker='o')
    plt.xlabel('Input Size')
    plt.ylabel('Time Complexity (seconds)')
    plt.title('Time Complexity of Huffman Encoding')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Sample usage for Huffman encoding and decoding
    input_symbols = ['A', 'A', 'B', 'C', 'C', 'C']
    encoded_text, codes = huffman_encoding(input_symbols)
    decoded_text = huffman_decoding(encoded_text, codes)

    print('Input symbols:', input_symbols)
    print('Huffman Codes:', codes)
    print('Encoded Text:', encoded_text)
    print('Decoded Text:', decoded_text)

    # Measure time complexity for different input sizes and plot the results
    input_sizes = [10, 100, 1000, 10000]  # Example input sizes
    time_complexity = measure_time_complexity(input_sizes)
    plot_time_complexity(input_sizes, time_complexity)
