import socket

user_credentials = {
    "user":"passwort"
}

def client_handler(client_socket):
    try:
        credentials = client_socket.recv(1024).decode().strip()

        if ":" in credentials:
            username, password = credentials.split(':',1)
            if user_credentials.get(username) == password:
                client_socket.send(b"Login successful")
            else:
                client_socket.send(b"Invalid Login")
        else:
            client_socket.send(b"Invalid Format")
    except Exception as e:
        print("Error beim client handling")
    # * Im auge behalten
    finally:
        client_socket.close()
        #                                                             IPv4                       TCP-Protokoll
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "127.0.0.1"
port = 44444

server.bind((server_ip, port))
server.listen(7)
print("[*] Server gestartet")

while True:
    client_socket, addr = server.accept()
    print(f"[*] Verbindung eingetroffen von IP: {addr}")#:PORT
    client_handler(client_socket)
