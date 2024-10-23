from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Load the PEM public key using cryptography
pem_key = '''
-----BEGIN PUBLIC KEY-----
MDcwDQYJKoZIhvcNAQEBBQADJgAwIwIcCWgnCB+TkBJ54MF0749g4n85qe001xM5
m5jtZQIDAQAB
-----END PUBLIC KEY-----
'''

try:
    public_key = serialization.load_pem_public_key(
        pem_key.encode(),
        backend=default_backend()
    )

    # Extract the modulus
    numbers = public_key.public_numbers()
    modulus = numbers.n
    print(f"Modulus (N): {modulus}")
except ValueError as e:
    print(f"Failed to parse RSA key: {e}")
