import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
from b_config import DB_PATH

IST = ZoneInfo("Asia/Kolkata")

def ist_now():
    """Return current IST time as string"""
    return datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")

def create_connection():
    """Create and return a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
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
            persona     TEXT    DEFAULT '',
            course      TEXT    DEFAULT '',
            timestamp   TEXT    
        )
    """)

    # ✅ Feedback table for evaluation results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id    TEXT    NOT NULL,
            final_score   REAL,
            groq_score  REAL,
            keyword_score REAL,
            tone_score    REAL,
            summary       TEXT,
            timestamp     TEXT    
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database tables ready")

def get_all_sessions():
    """Get all unique sessions with metadata for session picker"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT session_id, persona, course,
               MIN(timestamp) as started_at,
               COUNT(*) as turns
        FROM conversations
        GROUP BY session_id
        ORDER BY started_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "session_id": row["session_id"],
            "persona":    row["persona"],
            "course":     row["course"],
            "started_at": row["started_at"],
            "turns":      row["turns"]
        }
        for row in rows
    ]                                                                                                                                                                                                                                                                                                                                                                                                                                                       

def get_conversation(session_id: str, limit: int = 999):
    """Get last N conversation turns"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT salesperson, student, persona, course, timestamp
        FROM conversations
        WHERE session_id = ?
        ORDER BY id DESC 
        LIMIT ?
    """, (session_id, limit,))

    rows = cursor.fetchall()
    conn.close()

    # ✅ Reverse to get chronological order
    history = [
        {"salesperson": row["salesperson"], "student": row["student"], "persona": row["persona"], "course": row["course"], "timestamp":   row["timestamp"]}
        for row in reversed(rows)
    ]
    return history


def save_conversation(
    session_id: str,
    salesperson_msg: str,
    student_msg: str,
    persona: str = "",
    course: str = ""
):
    """Save one conversation turn to database"""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations (session_id, salesperson, student, persona, course, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, salesperson_msg, student_msg, persona, course, ist_now()))

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


def save_feedback(session_id: str, score: float, groq_score: float = 0, keyword_score: float = 0, tone_score: float = 0, summary: str = ""):
    """Save evaluation result to database"""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (session_id, final_score, groq_score, keyword_score, tone_score, summary, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (session_id, score, groq_score, keyword_score, tone_score, summary, ist_now()))

    conn.commit()
    conn.close()


def get_feedback_history(session_id: str):
    """Get all past feedback records"""
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT final_score, groq_score, keyword_score, tone_score, summary, timestamp
        FROM feedback
        WHERE session_id = ?
        ORDER BY id DESC
    """, (session_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "final_score":   row["final_score"],
            "groq_score":  row["groq_score"],
            "keyword_score": row["keyword_score"],
            "tone_score":    row["tone_score"],
            "summary": row["summary"],
            "timestamp": row["timestamp"]
        }
        for row in rows
    ]
