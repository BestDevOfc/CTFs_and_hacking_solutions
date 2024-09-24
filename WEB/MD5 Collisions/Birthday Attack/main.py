import hashlib

# these strings if hashed to MD5 will NOT collide.
# BUT, if you convert them to binary and once their digest is created in MD5 it WILL result in the same hash:
'''
hashlib.md5(bytearray.from_hex("STRING HERE")).digest()
creds: https://crypto.stackexchange.com/questions/1434/are-there-two-known-strings-which-have-the-same-md5-hash-value

'''
strings = {
    'lol.pdf': '0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef',
    'lol2.pdf': '0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef'
}
for fname, string in strings.items():
    binary = bytearray.fromhex(f"{string}")
    with open(f"{fname}", 'wb') as f:
        f.write(binary)
print(f"[ Done. ]")
    