import sqlite3
import hashlib


def create_db():
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """
    )
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS collections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        collection_name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """
    )
    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        (username, hashed_password),
    )
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_collections(user_id):
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT collection_name FROM collections WHERE user_id = ?", (user_id,)
    )
    collections = cursor.fetchall()
    conn.close()
    return [collection[0] for collection in collections]


def add_collection_to_user(user_id, collection_name):
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO collections (user_id, collection_name) VALUES (?, ?)",
        (user_id, collection_name),
    )
    conn.commit()
    conn.close()
