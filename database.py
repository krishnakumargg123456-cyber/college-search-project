import sqlite3

conn = sqlite3.connect("database/colleges.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS colleges(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    course TEXT,
    fees INTEGER,
    placement REAL,
    state TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS colleges(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    course TEXT,
    fees INTEGER,
    placement REAL,
    state TEXT,
    description TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS saved_colleges(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    college_id INTEGER
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")