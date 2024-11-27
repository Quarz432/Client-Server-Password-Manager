import socket
import threading
import sys
import sqlite3




class Server:
    def __init__(self):
        self.server_ip = "127.0.0.1"
        self.port = 52000
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.port))
        self.server_socket.listen(7)
        print("[*] Server gestartet")
        self.lock = threading.Lock()


        try:
            self.conn = sqlite3.connect('C:\\Users\\Alico\\Documents\\GitHub\\Client-Server-Password-Manager\\passwort_manager.db', check_same_thread=False)
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
            print("3. Account anzeigen")
            print("0. Server herunterfahren")
            choice = input("Bitte wähle deine Option: ")
            if choice == "1":
                self.account_erstellen()
            elif choice == "2":
                self.account_loeschen()
            elif choice == "3":
                self.account_anzeigen()
            elif choice == "0":
                sys.exit()
            else:
                print("Keine der angegebenen Menü Optionen ausgewählt.")

    def verbindung_annehmen(self):
        while True:
            self.client_socket, addr = self.server_socket.accept()
            # print(f"[*] Verbindung eingetroffen von IP: {addr}")#:PORT
            self.client_handler()

    def account_erstellen(self):
        benutzername = input("Geben Sie ihren Benutzernamen ein: ")
        passwort = input("Geben Sie ihr Passwort ein: ")
        try:
            self.cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (benutzername, passwort))
            self.conn.commit()
        except Exception as e:
            print("ERR","Database Insertion Error", e)

    def account_anzeigen(self):
        self.cursor.execute("SELECT * FROM users")
        result = self.cursor.fetchall()
        print(result)

    def account_loeschen(self):
        accountname = input("Geben Sie ihren Benutzernamen ein: ").strip()
        if not accountname:
            print("Eingabe darf nicht Leer sein.")

        try:
            self.cursor.execute("SELECT * FROM users WHERE username = ?", (accountname,))
            checkname = self.cursor.fetchone()
        except Exception as e:
            print("ERR","Database Insertion Error", e)

        if not checkname:
            print("Accountname existiert nicht.")

        try:
            self.cursor.execute("DELETE FROM users WHERE username = ?", (accountname,))
            self.conn.commit()
        except Exception as e:
            print("ERR","Database Connection Error", e)
        finally:
            print(f"Der Account {accountname} wurde gelöscht.")

    def client_menue(self):


    def client_handler(self):
        try:
            credentials = self.client_socket.recv(1024).decode().strip()

            if ":" in credentials:
                username, password = credentials.split(':')
                try:
                    self.cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username,password))
                    result = self.cursor.fetchone()
                    if result:
                        self.client_socket.send(b"Login successful")
                        self.client_socket.send(r'''
                                                     ___                              _     __  __                             
                                                    | _ \__ _ _______ __ _____ _ _ __| |___|  \/  |__ _ _ _  __ _ __ _ ___ _ _ 
                                                    |  _/ _` (_-<_-< V  V / _ \ '_/ _` |___| |\/| / _` | ' \/ _` / _` / -_) '_|
                                                    |_| \__,_/__/__/\_/\_/\___/_| \__,_|   |_|  |_\__,_|_||_\__,_\__, \___|_|  
                                                                                                                 |___/
                                            '''.encode())
                        self.client_socket.send(r'''
                        [1] Accounts anzeigen
                        [2] Account hinzufügen
                        [3] Account löschen
                        [4] Account bearbeitet
                        [0] Sitzung Beenden
                        '''.encode())

                        benutzer_menuauswahl = self.client_socket.recv(1024).decode()
                        if benutzer_menuauswahl == "1":
                            try:
                                self.cursor.execute("SELECT u.username, p.service, p.service_username, p.service_passwort FROM users u JOIN passwords p on u.id = p.user_id WHERE u.username = ?", (username,))
                                self.conn.commit()
                                login_data = self.cursor.fetchall()

                                resultat = ""  # Leerer Startstring
                                separator = ":"  # Separator

                                for index, element in enumerate(login_data):
                                    if index == 0:
                                        resultat += element  # Erster Eintrag ohne Separator
                                    else:
                                        resultat += separator + element  # Separator hinzufügen
                                print(resultat)

                                with self.lock:
                                    self.client_socket.send(resultat.encode())

                            except Exception as e:
                                print("ERR","Database Error Dienste anzeigen und sendne fehlgeschlagen", e)

                        elif benutzer_menuauswahl == "2":
                            try:
                                with self.lock:
                                    self.client_socket.send("Bitte geben Sie den Anbieter an: ".encode())
                                    anbieter = self.client_socket.recv(1024).decode()
                                    self.client_socket.send("Bitte geben Sie den Benutzernamen an: ".encode())
                                    benutzername = self.client_socket.recv(1024).decode()
                                    self.client_socket.send("Bitte geben Sie das Passwort an: ".encode())
                                    passwort = self.client_socket.recv(1024).decode()
                                    self.cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
                                    id = self.cursor.fetchone()
                                    self.cursor.execute("INSERT INTO passwords (id, service, service_username, service_passwort) VALUES (?,?,?)", (id[0], anbieter,benutzername,password))
                                    self.conn.commit()
                            except Exception as e:
                                print("ERR","Connection Error", e)
                    else:
                        self.client_socket.send(b"Invalid Login")
                except Exception as e:



                    print("ERR","Database Insertion Error", e)
            else:
                self.client_socket.send(b"Invalid Format")

        # * Im auge behalten
        finally:
            self.client_socket.close()

server = Server()




