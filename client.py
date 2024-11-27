import socket
#                                                             IPv4                              TCP-Protokoll
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "127.0.0.1"
port = 52000

client_socket.connect((server_ip, port))

benutzername = input("Bitte gebe einen Benutzernamen ein: ")
passwort = input("Bitte gebe ein Passwort ein: ")

daten_zum_übermitteln = f"{benutzername}:{passwort}"

client_socket.send(daten_zum_übermitteln.encode())
#Antwort entgegen
while True:
    response = client_socket.recv(1024)
    print(response.decode())
    answer = input()
    client_socket.send(answer.encode())