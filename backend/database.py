import sqlite3
from datetime import datetime
from config import DB_PATH

def create_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # ✅ allows dict-like access
    return conn

def create_tables():
    """Create all required tables if they don't exist"""
    conn = create_connection()
    cursor = conn.cursor()

    # ✅ Conversations table with all needed columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id  TEXT    NOT NULL,      
            salesperson TEXT    NOT NULL,
            student     TEXT    NOT NULL,
            persona     TEXT    DEFAULT 'Beginner',
            course      TEXT    DEFAULT '',
            timestamp   TEXT    DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ✅ Feedback table for evaluation results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id    TEXT    NOT NULL,
            final_score   REAL,
            gemini_score  REAL,
            keyword_score REAL,
            tone_score    REAL,
            summary       TEXT,
            timestamp     TEXT    DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database tables ready")

def get_conversation(session_id: str, limit: int = 10):
    """Get last N conversation turns"""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT salesperson, student, persona, course 
        FROM conversations
        WHERE session_id = ?
        ORDER BY id DESC 
        LIMIT ?
    """, (session_id, limit,))

    rows = cursor.fetchall()
    conn.close()

    # ✅ Reverse to get chronological order
    history = [
        {"salesperson": row["salesperson"], "student": row["student"], "persona": row["persona"], "course": row["course"]}
        for row in reversed(rows)
    ]
    return history


def save_conversation(
    session_id: str,
    salesperson_msg: str,
    student_msg: str,
    persona: str = "Beginner",
    course: str = ""
):
    """Save one conversation turn to database"""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations (session_id, salesperson, student, persona, course)
        VALUES (?, ?, ?, ?, ?)
    """, (session_id, salesperson_msg, student_msg, persona, course))

    conn.commit()
    conn.close()


def clear_conversation(session_id: str):
    """Delete all conversation history"""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM conversations WHERE session_id = ?",
        (session_id,)
    )

    conn.commit()
    conn.close()
    print("🗑️ Conversation history cleared")


def save_feedback(session_id: str, score: float, gemini_score: float = 0, keyword_score: float = 0, tone_score: float = 0, summary: str = ""):
    """Save evaluation result to database"""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (session_id, final_score,
            gemini_score,
            keyword_score,
            tone_score, summary)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, score,
            gemini_score,
            keyword_score,
            tone_score, summary))

    conn.commit()
    conn.close()


def get_feedback_history(session_id: str):
    """Get all past feedback records"""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT final_score,
            gemini_score,
            keyword_score,
            tone_score, summary, timestamp
        FROM feedback
        WHERE session_id = ?
        ORDER BY id DESC
    """, (session_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "final_score":   row["final_score"],
            "gemini_score":  row["gemini_score"],
            "keyword_score": row["keyword_score"],
            "tone_score":    row["tone_score"],
            "summary": row["summary"],
            "timestamp": row["timestamp"]
        }
        for row in rows
    ]