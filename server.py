import socket
import ssl
import threading
import os
from datetime import datetime
 
# ── Config ────────────────────────────────────────────────────────────────────
HOST        = "0.0.0.0"
PORT        = 5001
FILE_NAME   = "testfile.bin"
BUFFER_SIZE = 65536   # 64 KB — much faster than 1024
# ──────────────────────────────────────────────────────────────────────────────
 
# Track active connections (thread-safe)
active_clients = 0
lock = threading.Lock()
 
 
def log(msg):
    """Timestamped console log."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
 
 
def handle_client(conn, addr):
    """Handle a single client: send the file, then close the connection."""
    global active_clients
 
    with lock:
        active_clients += 1
 
    log(f"Connected: {addr}  |  Active clients: {active_clients}")
 
    try:
        # Validate file exists before attempting transfer
        if not os.path.isfile(FILE_NAME):
            log(f"ERROR: '{FILE_NAME}' not found — cannot serve client {addr}")
            return
 
        file_size = os.path.getsize(FILE_NAME)
        bytes_sent = 0
 
        with open(FILE_NAME, "rb") as f:
            while True:
                chunk = f.read(BUFFER_SIZE)
                if not chunk:
                    break
                conn.sendall(chunk)
                bytes_sent += len(chunk)
 
        log(f"Sent {bytes_sent}/{file_size} bytes to {addr} — transfer complete")
 
    except (BrokenPipeError, ConnectionResetError):
        # Client disconnected mid-transfer
        log(f"Client {addr} disconnected abruptly")
 
    except OSError as e:
        log(f"Socket error with {addr}: {e}")
 
    except Exception as e:
        log(f"Unexpected error with {addr}: {e}")
 
    finally:
        conn.close()
        with lock:
            active_clients -= 1
        log(f"Connection closed: {addr}  |  Active clients: {active_clients}")
 
 
def start_server():
    # Create TCP socket with SO_REUSEADDR so restarts don't fail
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)   # backlog bumped from 5 → 10
 
    # SSL context — TLS 1.2+ only, no legacy protocols
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")
 
    log(f"Secure server listening on {HOST}:{PORT}")
    log(f"Serving file: '{FILE_NAME}'  ({os.path.getsize(FILE_NAME) if os.path.isfile(FILE_NAME) else 'FILE NOT FOUND'})")
 
    try:
        while True:
            conn, addr = server_socket.accept()
 
            try:
                # Wrap with SSL before spawning thread
                secure_conn = context.wrap_socket(conn, server_side=True)
 
                thread = threading.Thread(
                    target=handle_client,
                    args=(secure_conn, addr),
                    daemon=True   # threads die automatically when main exits
                )
                thread.start()
 
            except ssl.SSLError as e:
                log(f"SSL handshake failed with {addr}: {e}")
                conn.close()   # close raw socket if SSL wrap failed
 
    except KeyboardInterrupt:
        log("Server shutting down...")
 
    finally:
        server_socket.close()
        log("Server socket closed")
 
 
if __name__ == "__main__":
    start_server()