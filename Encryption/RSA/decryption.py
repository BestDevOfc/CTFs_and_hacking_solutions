# for NCL gym
# Given values
p = 13  # Example value for p
q = 83  # Example value for q
e = 43  # Example value for e
ciphertext = [996, 894, 379, 631, 894, 82, 379, 852, 631, 677, 677, 194, 893]

# Step 1: Calculate n
n = p * q

# Step 2: Calculate Euler's Totient function φ(n)
phi_n = (p - 1) * (q - 1)

# Step 3: Calculate d (the modular inverse of e modulo φ(n))
from sympy import mod_inverse
d = mod_inverse(e, phi_n)

# Step 4: Decrypt the ciphertext
decrypted_message = ""
for c in ciphertext:
    decrypted_block = pow(c, d, n)  # Decrypt each block
    decrypted_message += chr(decrypted_block)  # Convert block to ASCII character

print(f"Decrypted message: {decrypted_message}")
