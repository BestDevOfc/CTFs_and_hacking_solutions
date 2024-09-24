import jwt

# Original header and payload
header = {
  "alg": "HS256",
  "typ": "JWT"
}

payload = {
  "exp": 1725314914,
  "iat": 1725314314,
  "role": "admin",
  "username": "lol"
}

key = "095cc0a35080ea1bef5a25eed478e020e82576ad"
alg = "HS256"
# Encode the JWT without a signature
token = jwt.encode(payload, key=key, algorithm=alg, headers=header)

print(f"JWT: {token}")
