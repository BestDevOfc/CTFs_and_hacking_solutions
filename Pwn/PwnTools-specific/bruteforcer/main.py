import itertools
import string

from pwn import*
from tqdm import tqdm

context.log_level = 'error'

# Get all lowercase letters
letters = string.ascii_lowercase

# Use itertools.product to generate all combinations of 4 letters
total_combinations = len(letters) ** 4
combinations = itertools.product(letters, repeat=4)

# Iterate over each combination and print it as a string
for combination in tqdm(combinations, total=total_combinations, desc="Processing Combinations"):
    binary_proc = process("chall")
    ingredient = ''.join(combination)
    binary_proc.sendline(ingredient.encode())
    resp = binary_proc.recvall()
    # print(f"[ Response Received: {resp} ]")
    if b'Wrong' in resp:
        # print(ingredient)
        ...
    else:
        print(f"[ SUCCESSFUL INGREDIENT; {ingredient} : {resp}]")
        open("SUCCESS.txt", 'a').write(f"{ingredient}\n")
        # break


