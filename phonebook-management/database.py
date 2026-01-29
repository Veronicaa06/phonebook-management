import sqlite3

DB_NAME = "contact_app.db"

def get_connection():
    """
    Tạo kết nối tới database SQLite (contact_app.db).
    Trả về đối tượng connection nếu thành công, None nếu thất bại.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None


def test_connection():
    """Test đơn giản kết nối database"""
    print("Testing database connection...")

    conn = get_connection()

    if conn is None:
        print("Connection failed")
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        if result and result[0] == 1:
            print("Connection and test query successful.")
            return True
        else:
            print("Test query failed")
            return False

    except sqlite3.Error as e:
        print(f"Query error: {e}")
        return False
    finally:
        conn.close()


def test_basic_query():
    """Test truy vấn cơ bản"""
    print("\nTesting basic queries...")

    conn = get_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        # Kiểm tra bảng contacts có tồn tại không (SQLite)
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='contacts'
        """)
        table_exists = cursor.fetchone()

        if table_exists:
            print("Bảng 'contacts' tồn tại")

            # Đếm số lượng contacts
            cursor.execute("SELECT COUNT(*) FROM contacts")
            count = cursor.fetchone()[0]
            print(f"Số lượng contacts: {count}")
        else:
            print("The 'contacts' table does not exist.")

        return True

    except sqlite3.Error as e:
        print(f"Query error: {e}")
        return False
    finally:
        conn.close()

def init_db():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                email TEXT,
                address TEXT
            )
        """)
        conn.commit()
        conn.close()


# Chạy các test
if __name__ == "__main__":
    print("=== START TESTING THE DATABASE (SQLITE) ===\n")

    connection_ok = test_connection()

    if connection_ok:
        test_basic_query()

    print("\n=== END OF TEST ===")
