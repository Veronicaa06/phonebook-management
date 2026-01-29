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
        print(f"Lỗi kết nối database: {e}")
        return None


def test_connection():
    """Test đơn giản kết nối database"""
    print("Đang test kết nối database...")

    conn = get_connection()

    if conn is None:
        print("Kết nối thất bại")
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        if result and result[0] == 1:
            print("Kết nối và truy vấn test thành công")
            return True
        else:
            print("Truy vấn test thất bại")
            return False

    except sqlite3.Error as e:
        print(f"Lỗi truy vấn: {e}")
        return False
    finally:
        conn.close()


def test_basic_query():
    """Test truy vấn cơ bản"""
    print("\nĐang test truy vấn cơ bản...")

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
            print("Bảng 'contacts' không tồn tại")

        return True

    except sqlite3.Error as e:
        print(f"Lỗi truy vấn: {e}")
        return False
    finally:
        conn.close()


# Chạy các test
if __name__ == "__main__":
    print("=== BẮT ĐẦU TEST DATABASE (SQLITE) ===\n")

    connection_ok = test_connection()

    if connection_ok:
        test_basic_query()

    print("\n=== KẾT THÚC TEST ===")
