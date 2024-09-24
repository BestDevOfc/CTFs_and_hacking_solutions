# PatriotCTF 2024 Pancakes

import time
from pwn import *
import base64

# Connect to the remote server
conn = remote('CHALLENGE_IP_HERE', PORT_HERE)

def decode_layers(string):
    try:
        string = base64.b64decode(string).decode().strip().rstrip()
        base64encoding, layers = string.split('|')
        for _ in range(int(layers)):
            base64encoding = base64.b64decode(base64encoding).decode()
        return base64encoding
    except Exception as e:
        print(f"The string -> {string}")
        input(f"Error in decode_layers: {e}")

# receive initial message w/ instructions
print(conn.recv())

solution = "NONE"
for i in range(1002):
    try:
        # Receive the challenge from the server
        time.sleep(0.1)
        print("at the top")
        challenge_message = conn.recv().decode().strip()
        print(challenge_message)
        if 'incorrect' in challenge_message.lower():
            print(f"[ Incorrect ! ]")
            break
        
        # parse the Base64
        challenge_message = challenge_message.split('Challenge: ')[1].split('(')[0].strip().rstrip()

        # decode all the layers and append the chall number + the alphanumeric solution we get
        solution = decode_layers(challenge_message) + "|" + str(i)
        print(f"SOLUTION: {solution}")

        if solution:
            conn.sendline(solution.encode())
        else:
            print("[Error] Solution is empty!")
            break
        
        time.sleep(0.1)  # Optional delay
    except Exception as err:
        input(f"In {i} - Error: {err}")
        input(f"{challenge_message}")