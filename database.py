import sqlite3

def init_db():
    conn = sqlite3.connect("records.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            weight REAL,
            sugar REAL,
            bp INTEGER,
            fever REAL,
            heartbeat INTEGER,
            pulse INTEGER,
            risk INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_record(name, age, weight, sugar, bp, fever, heartbeat, pulse, risk):
    conn = sqlite3.connect("records.db")
    c = conn.cursor()
    c.execute("INSERT INTO patients (name, age, weight, sugar, bp, fever, heartbeat, pulse, risk) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (name, age, weight, sugar, bp, fever, heartbeat, pulse, risk))
    conn.commit()
    conn.close()

def get_records():
    conn = sqlite3.connect("records.db")
    c = conn.cursor()
    c.execute("SELECT * FROM patients ORDER BY id DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return rows
