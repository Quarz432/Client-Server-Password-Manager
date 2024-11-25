import socket
#                             IPv4            TCP-Protokoll
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "127.0.0.1"
port = 44444

benutzername = input("Gebe den Nutzernamen ein: ")
passwort = input("Gebe das Passwort ein: ")



