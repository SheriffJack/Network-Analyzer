import socket
import time
import os
import csv
import schedule
from datetime import datetime

SERVER_IP = "127.0.0.1"
PORT = 5001
BUFFER_SIZE = 1024

DOWNLOAD_FILE = "downloaded.bin"
LOG_FILE = "network_log.csv"


def download_file():

    # Socket creation
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    client_socket.connect((SERVER_IP, PORT))

    start_time = time.time()

    with open(DOWNLOAD_FILE, "wb") as f:

        while True:

            # Receive data from server
            data = client_socket.recv(BUFFER_SIZE)

            if not data:
                break

            f.write(data)

    end_time = time.time()

    client_socket.close()

    return end_time - start_time


def calculate_speed(time_taken):

    file_size_mb = os.path.getsize(DOWNLOAD_FILE) / (1024 * 1024)

    speed = file_size_mb / time_taken

    return file_size_mb, speed


def log_results(hour, size, time_taken, speed):

    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        # Write header only once
        if not file_exists:
            writer.writerow(["Hour", "Size_MB", "Time_sec", "Speed_MBps"])

        writer.writerow([hour, size, time_taken, speed])


def run_download():

    print("\nStarting scheduled download...")

    time_taken = download_file()

    size, speed = calculate_speed(time_taken)

    hour = datetime.now().strftime("%H:%M")

    log_results(hour, size, time_taken, speed)

    print("Download complete")
    print("Time:", round(time_taken, 2), "seconds")
    print("Speed:", round(speed, 2), "MB/s")


# Schedule download every hour
schedule.every(1).minutes.do(run_download)

# For testing/demo you can temporarily use:
# schedule.every(1).minutes.do(run_download)

print("Network analyzer running...")

while True:

    schedule.run_pending()

    time.sleep(1)