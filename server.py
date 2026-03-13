import socket

HOST = "0.0.0.0"
PORT = 5001
FILE_NAME = "testfile.bin"
BUFFER_SIZE = 1024

# 1. Socket creation
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Binding socket to address and port
server_socket.bind((HOST, PORT))

# 3. Listening for incoming connections
server_socket.listen(5)

print("Server started and listening on port", PORT)

while True:

    # 4. Accept client connection
    conn, addr = server_socket.accept()
    print("Connection established with:", addr)

    try:
        with open(FILE_NAME, "rb") as f:

            while True:
                data = f.read(BUFFER_SIZE)

                if not data:
                    break

                # 5. Send data to client
                conn.sendall(data)

        print("File sent successfully")

    except Exception as e:
        print("Error:", e)

    finally:
        # 6. Close client connection
        conn.close()
        print("Connection closed\n")