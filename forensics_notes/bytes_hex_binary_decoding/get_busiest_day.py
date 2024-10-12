from datetime import datetime
from collections import defaultdict
import re

# Function to process the log file and find the busiest day
def find_busiest_day(log_file_path):
    with open(log_file_path, 'r') as file:
        log_content = file.read()

    # Initialize data structure to store bytes transferred per day
    bytes_per_day = defaultdict(int)

    # Regex to capture the timestamp and bytes transferred
    log_entry_pattern = re.compile(r'\[ Time Stamp: (\d+) \]\n\[ Bytes Transferred: (\d+)')

    # Process each log entry
    for match in log_entry_pattern.finditer(log_content):
        timestamp = int(match.group(1))
        day = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')  # Convert to day format
        bytes_transferred = int(match.group(2))
        bytes_per_day[day] += bytes_transferred

    # Find the day with the maximum bytes transferred
    busiest_day = max(bytes_per_day, key=bytes_per_day.get)
    return busiest_day, bytes_per_day[busiest_day]

# Example usage
log_file_path = 'decoded_sky_logs.txt'
busiest_day, total_bytes = find_busiest_day(log_file_path)
print(f"Busiest day: {busiest_day}, Total bytes: {total_bytes}")