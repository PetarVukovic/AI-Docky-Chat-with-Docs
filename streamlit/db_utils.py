import sqlite3
import hashlib


def create_db():
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()

    # Kreiranje tabele za korisnike ako ne postoji
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """
    )

    # Kreiranje tabele collections ako ne postoji
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS collections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            collection_name TEXT NOT NULL,
            document_type TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """
    )

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    create_db()  # Ensure the database and tables are created before any operation
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
    create_db()  # Ensure the database and tables are created before any operation
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
    create_db()  # Ensure the database and tables are created before any operation
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT collection_name, document_type FROM collections WHERE user_id = ?",
        (user_id,),
    )
    collections = cursor.fetchall()
    conn.close()
    return collections


def add_collection_to_user(user_id, collection_name, document_type):
    create_db()  # Ensure the database and tables are created before any operation
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO collections (user_id, collection_name, document_type) VALUES (?, ?, ?)",
        (user_id, collection_name, document_type),
    )
    conn.commit()
    conn.close()
