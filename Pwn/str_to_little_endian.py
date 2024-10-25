def string_to_little_endian_hex(input_string):
    # Add null terminator if needed
    if input_string[-1] != '\0':
        input_string += '\0'

    # Convert string to hex
    hex_rep = input_string.encode('utf-8').hex()

    # Split the hex string into chunks of 8 characters (4 bytes)
    chunks = [hex_rep[i:i+8] for i in range(0, len(hex_rep), 8)]

    # Reverse the order of each 4-byte chunk to achieve little-endian
    little_endian_chunks = [chunk[i:i+2] for chunk in chunks for i in range(0, len(chunk), 2)][::-1]

    # Join the reversed chunks to get the final little-endian hex representation
    little_endian_hex = ''.join(little_endian_chunks)

    return little_endian_hex

# Example usage:
input_string = "/bin/bash"
hex_output = string_to_little_endian_hex(input_string)
print(f"Little-endian hex: 0x{hex_output}")
