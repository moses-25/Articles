import sqlite3

def get_connection():
    try:
        conn = sqlite3.connect('articles.db')
        conn.row_factory = sqlite3.Row  
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None