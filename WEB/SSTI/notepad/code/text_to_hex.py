import binascii

text = "_"
hex_representation = binascii.hexlify(text.encode()).decode()
print(hex_representation)  # Output: 48656c6c6f2c20576f726c6421
