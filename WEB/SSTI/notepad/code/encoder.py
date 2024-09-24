# *** DID NOT NEED TO URL ENCODE because filename only stores first 128 (could've just put plain ASCII 'A'*128)
import urllib.parse
from werkzeug.urls import url_fix

string_to_encode = "Hello World!"

string = open("data.txt", 'r').read()
url_fixed = url_fix(string)
url_encoded = urllib.parse.quote(url_fixed)
print(url_encoded)

