"""
log_processor.py

Description:
This script reads a Moddable instrumentation log file, extracts information related to "instruments" from each line,
and organizes the data into separate CSV files for a "worker" and "controller" virtual machines.

Usage:
1. Update the 'input_file', 'worker_file', and 'controller_file' variables with the appropriate file paths.
2. Run the script.

Dependencies:
- Python 3

"""
import re
import time
from datetime import datetime

WORKER_CSV_HEADER = "timestamp,Chunk used,Chunk available,Slot used,Slot available,Stack used,Stack available,Garbage collections,Keys used,Modules loaded,Parser used,Floating Point\n"
CONTROLLER_CSV_HEADER = "timestamp,Pixels drawn,Frames drawn,Network bytes read,Network bytes written,Network sockets,Timers,Files,Poco display list used,Piu command List used,SPI flash erases,System bytes free,CPU 0,CPU 1,Chunk used,Chunk available,Slot used,Slot available,Stack used,Stack available,Garbage collections,Keys used,Modules loaded,Parser used,Floating Point\n"

"""
Convert a timestamp string to Unix timestamp in milliseconds.

Args:
- timestamp_str (str): Timestamp in the format "%b %d %H:%M:%S".

Returns:
- int: Unix timestamp in milliseconds.
"""
def convert_to_unix_timestamp(timestamp_str):
    dt = datetime.strptime(timestamp_str, "%b %d %H:%M:%S")
    dt = dt.replace(year=datetime.now().year)
    return int(dt.timestamp())

"""
Parse a log line and extract relevant information.

Args:
- line (str): Log line to be parsed.

Returns:
- Tuple: A tuple containing (key, timestamp, data).
    - key (str): "worker" or "controller".
    - timestamp (str): Timestamp string.
    - data (str): Data string.
"""
def parse_log_line(line):
    if "instruments:" in line:
        match = re.match(r'(\d+) instruments: (.+)', line)
        if match:
            timestamp, data = match.groups()
            timestamp = int(timestamp)
            data_items = data.split(',')
            if len(data_items) == 11:
                return "worker", timestamp, data
            elif len(data_items) == 24:
                return "controller", timestamp, data
    return None, None, None

"""
Write logs to a CSV file.

Args:
- logs (list): List of log entries.
- output_file (str): Output CSV file path.
- header (str): CSV file header.
"""
def write_logs_to_file(logs, output_file, header):
    with open(output_file, 'w') as output:
        output.write(header)
        for log in logs:
            output.write(log + "\n")

"""
Process the log file, extract relevant information, and write to CSV files.

Args:
- input_file (str): Input log file path.
- worker_file (str): Output CSV file path for worker component.
- controller_file (str): Output CSV file path for controller component.
"""
def process_log(input_file, worker_file, controller_file):
    worker_logs = []
    controller_logs = []

    with open(input_file, 'r') as file:
        for line in file:
            key, timestamp, data = parse_log_line(line)
            if key:
                # unix_timestamp = convert_to_unix_timestamp(timestamp)
                escaped_data = data.replace('"', r'\"')  # Escapa as aspas na string
                log_entry = f'{timestamp}, {escaped_data.strip()}'
                if key == "worker":
                    worker_logs.append(log_entry)
                else:
                    controller_logs.append(log_entry)


    write_logs_to_file(worker_logs, worker_file, WORKER_CSV_HEADER)
    write_logs_to_file(controller_logs, controller_file, CONTROLLER_CSV_HEADER)

if __name__ == "__main__":
    input_file = "nonMem.log"
    worker_file = "database/worker_file2.csv"
    controller_file = "database/controller_file2.csv"

    count = 0
    while True:
        count += 1
        print(f'Logging for {count} seconds')
        process_log(input_file, worker_file, controller_file)
        time.sleep(1)
