import sqlite3

conn = sqlite3.connect("auth.db")
cursor = conn.cursor()

# create user table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()