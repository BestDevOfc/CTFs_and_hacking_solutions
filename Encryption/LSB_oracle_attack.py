from pwn import *
from Crypto.Util.number import long_to_bytes
import re

# Server connection details
HOST = '0.cloud.chals.io'
PORT = 19108

def get_lsb(ciphertext):
    """Send the ciphertext to the server and get the least significant bit of the decrypted message."""
    r.recvuntil(b"Give me something to decrypt: ")  # Expect the server prompt
    r.sendline(str(ciphertext).encode())  # Ensure the ciphertext is sent as a string in byte form
    response = r.recvline().strip()
    try:
        return int(response)  # Convert the response to an integer (it should be 0 or 1)
    except ValueError:
        print(f"Unexpected server response: {response}")
        return None

def rsa_lsb_oracle_attack(n, e, c):
    """Perform the LSB oracle attack."""
    lower_bound = 0
    upper_bound = n
    factor = pow(2, e, n)  # Calculate 2^e mod n
    ciphertext = c

    for _ in range(n.bit_length()):
        # Multiply the ciphertext by 2^e mod n to shift the message
        ciphertext = (ciphertext * factor) % n
        lsb = get_lsb(ciphertext)

        if lsb is None:
            print("Exiting due to unexpected server response")
            break

        # Adjust bounds based on the LSB
        midpoint = (lower_bound + upper_bound) // 2
        if lsb == 0:
            upper_bound = midpoint
        else:
            lower_bound = midpoint

    # Recover the plaintext message
    return long_to_bytes(lower_bound)

# Connect to the remote service
r = remote(HOST, PORT)

# First, retrieve the public key and ciphertext
r.recvuntil(b"Public Key: ")
public_key = r.recvline().decode()

# Use regular expressions to extract the values of n and e
match = re.search(r"n=(\d+), e=(\d+)", public_key)
n = int(match.group(1))
e = int(match.group(2))

r.recvuntil(b"Ciphertext: ")
c = int(r.recvline().decode().strip())

# Now, perform the LSB oracle attack to recover the flag
flag = rsa_lsb_oracle_attack(n, e, c)
if flag:
    print(f"Recovered flag: {flag.decode()}")

r.close()
