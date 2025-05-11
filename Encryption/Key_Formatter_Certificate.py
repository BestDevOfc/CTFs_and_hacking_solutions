'''

    To easily pad keys and stuff, needed this for a SAMLResponse forgery CTF

'''

def format_key( key: str, keyword: str ) -> str:
    character_count = 0
    formatted_key = ''
    for character in key:
        character_count += 1

        formatted_key += f"{character}"
        print(character_count)
        # have to do 64 character 'padding'
        if character_count / 64 == 1:
            formatted_key += '\n'
            character_count = 0
        
    # NOTE: the "CETIFICATE" keyword may change depending on context, for example it could be "RSA PRIVATE KEY"
    return f"-----BEGIN {keyword}-----\n{formatted_key}\n-----END {keyword}-----\n"


def main():
    raw_certificate = open("raw_certificate.txt", 'r', encoding="utf-8").read()
    with open("cert.pem", "w") as f:
        f.write(format_key(raw_certificate, "CERTIFICATE"))

if __name__ == "__main__":
    main()



