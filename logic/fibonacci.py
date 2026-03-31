# Transform char into decimal in ASCII table
def text_to_decimals(text: str) -> list[int]:
    return [ord(char) for char in text]

text = input("Choose something: ")
decimal_text = text_to_decimals(text)

print(decimal_text)

for i in decimal_text:
    print(i)

def fibonacci_skip_first_two(n):
    if n <= 2:
        return []

    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
        
    return sequence[2:]

print(fibonacci_skip_first_two(14))