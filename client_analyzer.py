import socket
import ssl
import time
import csv
import schedule
from datetime import datetime
import os

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001
OUTPUT_FILE = "downloaded_file.bin"
CSV_FILE = "network_log.csv"


def download_file():

    try:
        start_time = time.time()

        # TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # SSL context
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        secure_sock = context.wrap_socket(sock)

        secure_sock.connect((SERVER_HOST, SERVER_PORT))

        total_bytes = 0

        with open(OUTPUT_FILE, "wb") as f:
            while True:
                data = secure_sock.recv(4096)
                if not data:
                    break
                f.write(data)
                total_bytes += len(data)

        end_time = time.time()
        secure_sock.close()

        duration = end_time - start_time
        speed = total_bytes / duration / (1024 * 1024)

        print(f"\n[{datetime.now()}]")
        print(f"Downloaded {total_bytes} bytes")
        print(f"Time: {duration:.2f} sec")
        print(f"Speed: {speed:.2f} MB/s")

        log_result(duration, speed)

    except Exception as e:
        print("Download failed:", e)


def log_result(duration, speed, total_bytes):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            round(total_bytes / (1024*1024), 4),  # Size in MB
            round(duration, 4),
            round(speed, 4)
        ])


def job():
    print("\nStarting scheduled download...")
    download_file()


#FOR DEMO
schedule.every(1).minutes.do(job)

# For actual requirement:
# schedule.every().hour.do(job)

print("SSL Network Analyzer Running...")

while True:
    schedule.run_pending()
    time.sleep(1)
