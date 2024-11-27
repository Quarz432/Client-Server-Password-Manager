import sqlite3

def init_db():
    conn = sqlite3.connect('passwort_manager.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY  AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY  AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        service TEXT NOT NULL,
        service_username TEXT,
        service_passwort TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')

    conn.commit()
    conn.close()


init_db()