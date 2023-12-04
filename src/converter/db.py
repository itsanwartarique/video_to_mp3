import sqlite3

conn = sqlite3.connect("../db/audio.db")
cursor = conn.cursor()

# vidoes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mp3 (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        mp3_data BLOB
    )
''')

conn.commit()
conn.close()