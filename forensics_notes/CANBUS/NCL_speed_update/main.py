'''
used this for testing, otherwise we'd be doing a blind processing script, not smart
since accuracy actually matters for NCL.
calc_mph(b"0000c01aa8000013")
"0000c01aa8000013"
"00 00 c0 1a a8 00 00 13"

0x1a << 8
6656

6656 + 0xa8
6824

6824/100
68.24

68.24 * 0.6213751
42.40263682399999
'''


def calc_mph(hex_string: bytes) -> float:
    hex_string = hex_string.decode("utf8")    
    count = 0
    new_hex_string = ''
    # converting the hex string to xx xx xx xx format instead of xxxxxx...
    for character in hex_string:
        if count == 2:
            count = 0
            new_hex_string += f" {character}"
            count += 1
        else:
            new_hex_string += character
            count += 1
    
    print(f"New Hex String: {new_hex_string}")

    speed_pos = 3
    hex_bytes_str = new_hex_string.split()
    
    # CONVERTIG HEX STRING INTO BASE16 INTEGER
    # double speed = frame->data[speed_pos] << 8; (same as multiplying the int base 16 value by 256 )
    speed = int(hex_bytes_str[ speed_pos ], 16) << 8
    # print(f"Speed: {speed}")

    # speed += frame->data[speed_pos + 1];
    speed += int(hex_bytes_str[ speed_pos + 1], 16)
    # print(f"Speed: {speed}")

    # speed = speed / 100;
    speed /= 100
    # print(f"Speed: {speed}")

    # speed = speed * 0.6213751;
    speed *= 0.6213751
    # print(f"Speed: {speed}")

    return speed


def main():
    # Open and read the CSV file
    speed_id = b"589"
    data = open("data.csv", 'rb').readlines()
    mphs = []
    # Iterate through each line in the CSV
    for line in data[1:]:
        try:
            can_bus_id = line.split(b',')[6]
            if speed_id not in can_bus_id:
                '''
                    REMEMBER*** we only want the update ID,
                    this is because can_bud broadcasts to all components kind of like
                    ARP does when trying to figure out who's IP belongs to which 
                    mac address. 

                    As a result, we're only interested in the 589 canbus ID because we know this is 
                    the one for the speed update from the code they gave us!
                '''
                continue
            # Extract the 9th field (index 8) and remove quotes
            hex_string = line.split(b',')[8].replace(b'"', b'')
            print(f"Hex String: {hex_string}")
            mph = calc_mph(hex_string)
            print(f"MPH: {mph}")
            mphs.append(mph)
            


        except Exception as err:
            print(f"{err}")
    print(f"[ The maximum MPH update given to a car ]: {max(mphs)}")
    # 20.13

if __name__ == "__main__":
    main()