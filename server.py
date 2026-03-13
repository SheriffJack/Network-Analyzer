import socket
import threading

HOST = "0.0.0.0"
PORT = 5001
FILE_NAME = "testfile.bin"
BUFFER_SIZE = 1024


def handle_client(conn, addr):

    print("Client connected:", addr)

    try:
        with open(FILE_NAME, "rb") as f:

            while True:

                data = f.read(BUFFER_SIZE)

                if not data:
                    break

                conn.sendall(data)

        print("File sent to", addr)

    except ConnectionResetError:
        print("Client disconnected abruptly:", addr)

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()
        print("Connection closed:", addr)


# socket creation
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind
server_socket.bind((HOST, PORT))

# listen
server_socket.listen(5)

print("Server running on port", PORT)

while True:

    # accept connection
    conn, addr = server_socket.accept()

    # create new thread
    client_thread = threading.Thread(
        target=handle_client,
        args=(conn, addr)
    )

    client_thread.start()