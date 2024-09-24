'''**** you can use RSACTFROOL to do the same thing !!!! ****'''


'''
[+] Mind your Ps and Qs (having a small N value decrypter):
[+] to get prime factors I used: https://factordb.com
Decrypt my super sick RSA:
c: 861270243527190895777142537838333832920579264010533029282104230006461420086153423
n: 1311097532562595991877980619849724606784164430105441327897358800116889057763413423
e: 65537

Decrupted Message: picoCTF{sma11_N_n0_g0od_13686679}
'''

def convert_hex_to_ascii( hex_number: int ) -> str:
    try:
        # \x is being "spliced out", hence the "2:"
        plaintext = bytearray.fromhex(hex(hex_number)[2:]).decode()
        return plaintext
    except Exception as err:
        print(f"[ When converting the HEX->bytearray->ASCII the following exception was raied ] --> {err}")
    return "Err"
    

ciphertext = 861270243527190895777142537838333832920579264010533029282104230006461420086153423
modulus_n = 1311097532562595991877980619849724606784164430105441327897358800116889057763413423 # vulnerability is here, bcs it's small
                                                                                                # (just over 100 bits)
                                                                                                # bcs of this we can factor it
public_encryption_exponent = 65537 # it's normal for this value to be small
# if you get more than 2 numbers or they're not odd then it's incorrect!
p = 1955175890537890492055221842734816092141 # factor % 2 = 1 (is prime factor, good)
q = 670577792467509699665091201633524389157003 # factor % 2 = 1 (is prime factor, good)

# now we need to derive phi_n which is what we'll use for calculating the priv8 key (d)
phi_n = (p-1)*(q-1) # interesting how subtracting them by 1 makes them now even numbers.. hmmm..
d = pow(public_encryption_exponent, -1, phi_n)

# now we have everything we need to decrypt our message
hex_number = pow(ciphertext, d, modulus_n)

# we need to convert the hex into ASCII to read it
print( convert_hex_to_ascii(hex_number) )
