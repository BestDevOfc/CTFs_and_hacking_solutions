import json
import binascii

'''

we didn't have secret key, but we know our cookie is a XOR ciphertext and we know
how the plaintext looks cuz of backend code.

code:
    user = {
        'username':user.username,
        'displays':user.displayname,
        'uid':user.uid
    }
    token = encode(dict(user))

'''

def derive_key(plaintext: dict, ciphertext_hex: str) -> bytes:
    # Convert the plaintext dictionary to a JSON string and encode it to bytes
    plaintext_bytes = json.dumps(plaintext).encode()
    
    # Convert the ciphertext (hex string) to bytes
    ciphertext_bytes = bytes.fromhex(ciphertext_hex)
    
    # XOR each byte of the plaintext with the corresponding byte of the ciphertext
    key = b''
    for p, c in zip(plaintext_bytes, ciphertext_bytes):
        key += bytes([p ^ c])
    
    return key

# Example usage:
plaintext =  {
    'username':'lol',
    'displays':'lol',
    'uid':1
}
ciphertext_hex = "48674c3731025651282f614a4d541a3d081a5e4760050a04075b080d277009534555021d6567585a0402107875504305"
derived_key = derive_key(plaintext, ciphertext_hex)

print(f"Derived Key: {derived_key}")
