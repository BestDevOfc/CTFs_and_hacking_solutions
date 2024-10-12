import datetime
import base64


# https://www.epochconverter.com/

def unix_to_UTC(unix):
    unix = int(f"{unix}".strip().rstrip())
    UTC = datetime.datetime.fromtimestamp(unix).strftime('%c').split()
    UTC = f"{UTC[0]} {UTC[1]} {UTC[2]}"
    return UTC

def hex_to_IPV4(hex: str):
    start, end = 0, 2
    IP_ADDR = ""
    byte_len = int(len(hex)/2)

    for iter in range(byte_len):        
        octet = int(hex[start:end], 16)
        IP_ADDR += f"{octet}"
        start = end
        end += 2
        IP_ADDR += '.'
    return IP_ADDR[:-1]



def decode_log(data: bytes):
    # truncating the magic bytes (8 bytes cut off)
    decoded_file = open("decoded_sky_logs.txt", 'w')
    data = data[8:]
    version_number = data[0]
    
    # get the next 4 bytes for the creation time stamp:
    # converting to an int from base16 hex.
    # just use some site to convert to UTC
    # creation_timestamp = unix_to_UTC(int(data[1:5].hex(), 15))
    creation_timestamp = int(data[1:5].hex(), 15)
    
    
    hostname_lenght = int(data[5:9].hex(), 16)
    hostname = data[9:9+hostname_lenght].hex()
    hostname = bytes.fromhex(hostname).decode("utf-8")
    
    start_index = 9+hostname_lenght
    flag_len = int(data[start_index:start_index+4].hex(), 16)
    start_index += 4
    
    flag = data[start_index:start_index+flag_len].hex()
    flag = bytes.fromhex(flag).decode("utf-8")
    flag = base64.b64decode(flag).decode("utf-8")
    start_index += flag_len
    
    num_entries = int(data[start_index:start_index+4].hex(), 16)
    start_index += 4
    
    decoded_file.write(f'''
============================================

[*] - Log Version Format: {version_number}
[*] - Creation Date: {creation_timestamp}
[*] - Host Name: {hostname}
[*] - Flag: {flag}
[*] - Num Entries: {num_entries}

============================================
''')
    
    total_bytes_transferred = 0
    ips = []
    ip_sent_freq = {}
    day_bytes_freq = {}
    # now parsing the log (body):
    for num_entry in range(num_entries):
        source_ip = data[start_index:start_index+4].hex()
        start_index += 4
        source_ip = hex_to_IPV4(source_ip)
        if source_ip not in ips:
            ips.append(source_ip)
        print(f"[ Source IP: {source_ip}")

        dest_ip = data[start_index:start_index+4].hex()
        start_index += 4
        dest_ip = hex_to_IPV4(dest_ip)
        if dest_ip not in ips:
            ips.append(dest_ip)
        print(f"[ Destination IP: {dest_ip} ]")


        # time_stamp = unix_to_UTC(int(data[start_index:start_index+4].hex(), 16))
        time_stamp = int(data[start_index:start_index+4].hex(), 16)
        print(f"[ Time Stamp: {time_stamp}")
        start_index += 4

        bytes_transferred = int(data[start_index:start_index+4].hex(), 16)
        start_index += 4
        if source_ip not in ip_sent_freq.keys():
            ip_sent_freq[source_ip] = bytes_transferred
        else:
            ip_sent_freq[source_ip] += bytes_transferred
        print(f"[ Bytes Transferred: {bytes_transferred}")
        
        total_bytes_transferred += bytes_transferred

        # if time_stamp not in day_bytes_freq.keys():
        #     day_bytes_freq[time_stamp] = bytes_transferred
        # else:
        #     day_bytes_freq[time_stamp] += bytes_transferred
        


        decoded_file.write(f'''
============================================
[*] Entry Number: {num_entry+1}
[ Source IP: {source_ip}
[ Destination IP: {dest_ip} ]
[ Time Stamp: {time_stamp} ]
[ Bytes Transferred: {bytes_transferred}
============================================
''')

        # input()

    # 
    most_sent_ip = "need_to_program"
    most_bytes = max(ip_sent_freq.values())
    for key, value in ip_sent_freq.items():
        if value == most_bytes:
            most_sent_ip = key
            break

    busy_day_bytes = max(day_bytes_freq.values())
    busiest_day = ""
    for key, value in day_bytes_freq.items():
        if value == busy_day_bytes:
            busiest_day = key
            break

    decoded_file.write(f"[ Total Bytes Transferred: {total_bytes_transferred:,} ]\n")
    decoded_file.write(f"[ Unique IPs: {len(ips):,} ]\n")
    decoded_file.write(f"[ IP that sent the most data: {most_sent_ip}; Bytes sent: {most_bytes:,} ]\n")
    # decoded_file.write(f"[ Busiest Day: {busiest_day}; bytes transferred: {busy_day_bytes} ]\n")
    decoded_file.close()


if __name__ == "__main__":
    data = open("SkyLogs.sky", 'rb').read()
    decode_log(data)
