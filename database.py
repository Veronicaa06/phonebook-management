import mysql.connector

def get_connection():
    """
    Tạo kết nối tới database contact_app.
    Trả về đối tượng connection nếu thành công, None nếu thất bại.
    """
    try:
        conn = mysql.connector.connect(
            host="db",
            user="root",
            password="27022006",  # Thay bằng mật khẩu thực tế
            database="contact_app"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Lỗi kết nối database: {e}")
        return None

def test_connection():
    """Test đơn giản kết nối database"""
    print("Đang test kết nối database...")

    # Test kết nối
    conn = get_connection()

    if conn is None:
        print("Kết nối thất bại")
        return False

    if conn.is_connected():
        print("Kết nối thành công")

        # Test truy vấn đơn giản
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        if result and result[0] == 1:
            print("Truy vấn test thành công")
        else:
            print("Truy vấn test thất bại")

        cursor.close()
        conn.close()
        return True
    else:
        print("Kết nối thất bại")
        return False


def test_basic_query():
    """Test truy vấn cơ bản"""
    print("\nĐang test truy vấn cơ bản...")

    conn = get_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        # Kiểm tra xem bảng contacts có tồn tại không
        cursor.execute("SHOW TABLES LIKE 'contacts'")
        table_exists = cursor.fetchone()

        if table_exists:
            print("Bảng 'contacts' tồn tại")

            # Đếm số lượng contacts
            cursor.execute("SELECT COUNT(*) FROM contacts")
            count = cursor.fetchone()[0]
            print(f"Số lượng contacts: {count}")
        else:
            print("Bảng 'contacts' không tồn tại")

        cursor.close()
        return True

    except mysql.connector.Error as e:
        print(f"Lỗi truy vấn: {e}")
        return False
    finally:
        if conn.is_connected():
            conn.close()

# Chạy các test
if __name__ == "__main__":
    print("=== BẮT ĐẦU TEST DATABASE ===\n")

    # Test kết nối
    connection_ok = test_connection()

    # Test truy vấn cơ bản
    if connection_ok:
        test_basic_query()

    print("\n=== KẾT THÚC TEST ===")

