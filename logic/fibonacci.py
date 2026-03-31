# # Transform char into decimal in ASCII table
# def text_to_decimals(text: str) -> list[int]:
#     return [ord(char) for char in text]

# text = input("Choose something: ")
# decimal_text = text_to_decimals(text)
# print(decimal_text)

# fibonacci_reverse = [233, 144, 89, 55, 34, 21, 13, 8, 5, 3, 2, 1]
# print(fibonacci_reverse)

# # fibonacci = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
# # print(fibonacci)

# encode = []

# for char in decimal_text:
#     for fibo_char in fibonacci_reverse:
#         if char <= fibo_char:
#             encode.append(0')
#         else:
#             aux = char
#             print(aux)
#             encode.append(1)
#             char = char - fibo_char
            
# print(encode)
            
# real_encode = encode.reverse()
# print(real_encode)

# transform char into decimal in ASCII table
def text_to_decimals(text: str) -> list[int]:
    return [ord(char) for char in text]


def fibonacci_encode(decimal: int) -> list[int]:
    fibonacci_reverse = [233, 144, 89, 55, 34, 21, 13, 8, 5, 3, 2, 1]
    bits = []

    for fibo in fibonacci_reverse:
        if decimal >= fibo:
            bits.append(1)
            decimal -= fibo
        else:
            bits.append(0)

    bits.reverse()  # reverse in place, then return separately
    return bits
    
    # return ''.join(str(bit) for bit in bits)

text = input("Choose something: ")
decimal_text = text_to_decimals(text)
print(f"Decimals: {decimal_text}")

encode = []

for decimal in decimal_text:
    bits = fibonacci_encode(decimal)
    encode.append(bits)  
    

print(f"Encode -> {encode}")