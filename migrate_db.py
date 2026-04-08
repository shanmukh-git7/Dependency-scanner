import sqlite3
import os

DB_PATH = "app.db"

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found. Skipping migration.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Add reset_token
        cursor.execute("ALTER TABLE users ADD COLUMN reset_token DATATYPE_TEXT")
        print("Added reset_token column")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("reset_token column already exists")
        else:
            print(f"Error adding reset_token: {e}")

    try:
        # Add reset_token_expiry
        cursor.execute("ALTER TABLE users ADD COLUMN reset_token_expiry DATATYPE_DATETIME")
        print("Added reset_token_expiry column")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("reset_token_expiry column already exists")
        else:
            print(f"Error adding reset_token_expiry: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
