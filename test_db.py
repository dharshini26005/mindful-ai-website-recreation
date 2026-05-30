import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
INSERT INTO applications
(name,email,phone,college,department,year,resume)
VALUES (?,?,?,?,?,?,?)
""", (
    "Test User",
    "test@gmail.com",
    "9999999999",
    "SNS",
    "CSE",
    "3rd Year",
    "resume.pdf"
))

conn.commit()

cursor.execute("SELECT * FROM applications")

print(cursor.fetchall())

conn.close()