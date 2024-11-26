import socket
import threading
import sys
import sqlite3


class Server:
    def __init__(self):
        self.server_ip = "127.0.0.1"
        self.port = 44444
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.port))
        self.server_socket.listen(7)
        print("[*] Server gestartet")

        try:
            self.conn = sqlite3.connect('passwort_manager.db', check_same_thread=False)
            self.cursor = self.conn.cursor()
        except Exception as e:
            print("ERR","Database Connection Error", e)

        self.server_thread = threading.Thread(target=self.verbindung_annehmen)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.menu()

    def menu(self):
        while True:
            print("1. Account erstellen")
            print("2. Account löschen")
            print("0. Server herunterfahren")
            choice = input("Bitte wähle deine Option: ")
            if choice == "1":
                self.account_erstellen()
            elif choice == "2":
                self.account_loeschen()
            elif choice == "0":
                sys.exit()
            else:
                print("Keine der angegebenen Menü Optionen ausgewählt.")

    def verbindung_annehmen(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            # print(f"[*] Verbindung eingetroffen von IP: {addr}")#:PORT
            self.client_handler(client_socket)

    def account_erstellen(self):
        benutzername = input("")
        passwort = input("")
        self.cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (benutzername, passwort))

    def account_loeschen(self):
            pass

    def client_handler(self,client_socket):
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

server = Server()




