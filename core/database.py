import sqlite3
import threading

DB_PATH = "database.db"
db_lock = threading.Lock()

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with db_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

def add_item(item_type, content):
    with db_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO history (type, content) VALUES (?, ?)", (item_type, content))
        conn.commit()
        conn.close()

def get_recent_items(limit=50):
    with db_lock:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, type, content FROM history ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [{"id": r[0], "type": r[1], "content": r[2]} for r in rows]