import sqlite3

conn = sqlite3.connect("../db/storage.db")
cursor = conn.cursor()

# vidoes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY,
        filename TEXT,
        video_data BLOB
    )
''')

conn.commit()
conn.close()