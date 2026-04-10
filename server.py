import socket
import ssl
import threading

HOST = "0.0.0.0"
PORT = 5001
FILE_NAME = "testfile.bin"
BUFFER_SIZE = 1024


def handle_client(conn, addr):

    print("Secure connection from:", addr)

    try:
        with open(FILE_NAME, "rb") as f:

            while True:
                data = f.read(BUFFER_SIZE)

                if not data:
                    break

                conn.sendall(data)

        print("File sent securely")

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()


# Create normal TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(5)

print("Secure server running on port", PORT)

# Create SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

context.load_cert_chain(certfile="server.crt", keyfile="server.key")

while True:

    conn, addr = server_socket.accept()

    try:
        # Wrap socket with SSL
        secure_conn = context.wrap_socket(conn, server_side=True)

        thread = threading.Thread(
            target=handle_client,
            args=(secure_conn, addr)
        )

        thread.start()

    except ssl.SSLError as e:
        print("SSL handshake failed:", e)