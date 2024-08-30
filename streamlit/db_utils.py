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
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            email_notifications BOOLEAN DEFAULT 0,
            theme TEXT DEFAULT 'System Default'
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


def register_user(username, password, email):
    create_db()
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed_password, email),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def login_user(username, password):
    create_db()
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute(
        "SELECT id, username, email, email_notifications, theme FROM users WHERE username = ? AND password = ?",
        (username, hashed_password),
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "email_notifications": bool(user[3]),
            "theme": user[4],
        }
    return None


def get_user_collections(user_id):
    create_db()
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT collection_name, document_type FROM collections WHERE user_id = ?",
        (user_id,),  # Osiguravamo da je user_id integer
    )
    collections = cursor.fetchall()
    conn.close()
    return collections


def add_collection_to_user(user_id, collection_name, document_type):
    create_db()
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO collections (user_id, collection_name, document_type) VALUES (?, ?, ?)",
        (user_id, collection_name, document_type),
    )
    conn.commit()
    conn.close()


def update_user_settings(user_id, settings):
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE users
            SET username = ?, email = ?, email_notifications = ?, theme = ?
            WHERE id = ?
        """,
            (
                settings["username"],
                settings["email"],
                settings["email_notifications"],
                settings["theme"],
                user_id,
            ),
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating user settings: {e}")
        return False
    finally:
        conn.close()


def get_user_by_id(user_id):
    conn = sqlite3.connect("user_collections.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, email, email_notifications, theme FROM users WHERE id = ?",
        (user_id,),
    )
    user = cursor.fetchone()
    conn.close()
    if user:
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "email_notifications": bool(user[3]),
            "theme": user[4],
        }
    return None
