# Function to implement the Extended Euclidean Algorithm
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Function to find the modular inverse
def modular_inverse(a, m):
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        return None  # Modular inverse does not exist
    else:
        # Return the result x mod m (ensure it's positive)
        return x % m


def main():
    message = "104 372 110 436 262 173 354 393 351 297 241 86 262 359 256 441 124 154 165 165 219 288 42 "[:-1].split()
    alphabet = "abcdefghijklmnopqrstuvwxyz".upper() # they wanted uppercase
    numbers = "0123456789" # wasn't doing this before, was using the original digits, which kept giving the wrong flag

    # # convert to integers
    message = [ int(element) for element in message ]

    modulus = 41
    mod_numbers = [ (number % modulus) for number in message ]

    modular_inverses = [ modular_inverse(mod_number, modulus) for mod_number in mod_numbers ]

    print("picoCTF{", end='')
    for number in modular_inverses:
        if number == 37:
            print('_', end='')
            continue
        if number >= 1 and number <= 26:
            print(alphabet[number-1], end='')
            continue
        if number >= 27 and number <= 36:
            print(numbers[number-27], end='')
            continue
    print("}")



if __name__ == "__main__":
    main()