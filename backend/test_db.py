import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def test_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT 1 AS test")
        result = cursor.fetchone()

        print("✅ Connection successful!")
        print("Result:", result)

        conn.close()

    except Exception as e:
        print("❌ Connection failed:")
        print(e)

if __name__ == "__main__":
    test_connection()
