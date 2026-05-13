import sqlite3

def create_connection():
    conn = sqlite3.connect("sales_training.db")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        salesperson TEXT,
        student TEXT
    )
    """)

    conn.commit()
    conn.close()
