import zlib
import os

def read_git_object(hash_id):
    # Read and decompress the object
    with open(hash_id, 'rb') as f:
        compressed_data = f.read()
        decompressed_data = zlib.decompress(compressed_data)
    
    # Git objects have a header like "blob <size>\0", followed by the actual content
    header_end = decompressed_data.find(b'\x00')
    if header_end == -1:
        raise ValueError(f"Invalid Git object format for {hash_id}")
    
    # Separate header and content
    header = decompressed_data[:header_end].decode('utf-8', errors='replace')
    content = decompressed_data[header_end + 1:]  # Content starts after the null byte
    
    return header, content

# Example usage
hash_id = 'HASH HERE'  # Replace with your SHA-1 hash
try:
    header, content = read_git_object(hash_id)
    print(f"Header: {header}")
    print(f"Content: {content}")  # Raw bytes
    print(f"Decoded Content (UTF-8): {content.decode('utf-8', errors='replace')}")
except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)
