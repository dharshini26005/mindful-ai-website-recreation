import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    college TEXT,
    department TEXT,
    year TEXT,
    resume TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully!")