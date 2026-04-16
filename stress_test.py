# stress_test.py
import threading
from client_analyzer import download_file

threads = [threading.Thread(target=download_file) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()