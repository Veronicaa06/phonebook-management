import tkinter as tk
from tkinter import messagebox
import database 

def validate_data(name, phone):
    """
    NFR-03: Validate Data - Kiểm tra tên không rỗng và số điện thoại đúng định dạng.
    """
    if not name.strip():
        messagebox.showerror("Lỗi", "Tên liên hệ không được để trống!") [cite: 10]
        return False
    
    # Kiểm tra số điện thoại chỉ chứa số 
    if not phone.isdigit():
        messagebox.showerror("Lỗi", "Số điện thoại chỉ được chứa các chữ số!") [cite: 10]
        return False
    
    if len(phone) < 10 or len(phone) > 11:
        messagebox.showerror("Lỗi", "Số điện thoại phải có từ 10-11 chữ số!") [cite: 10]
        return False
        
    return True

def save_contact_action(name_entry, phone_entry, email_entry, address_text, window):
    """
    Xử lý sự kiện khi bấm nút Save: Kiểm tra dữ liệu và lưu xuống DB.
    """
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_text.get("1.0", "end-1c")

    if validate_data(name, phone):
        conn = database.get_connection() [cite: 2]
        if conn:
            try:
                cursor = conn.cursor()
                # Query dựa trên các cột Thiên Anh đã thiết kế 
                sql = "INSERT INTO contacts (full_name, phone_number, email, address) VALUES (%s, %s, %s, %s)"
                val = (name, phone, email, address)
                cursor.execute(sql, val)
                conn.commit()
                messagebox.showinfo("Thành công", "Đã thêm liên hệ mới!")
                window.destroy()  
            except Exception as e:
                messagebox.showerror("Lỗi Database", f"Không thể lưu: {e}")
            finally:
                conn.close()

def search_contact_logic(search_entry, treeview):
    """
    Nhiệm vụ: Khi bấm Search -> Lọc dữ liệu hiển thị.
    """
    search_query = search_entry.get().strip()
    
    # Xóa dữ liệu cũ trên bảng hiển thị 
    for item in treeview.get_children():
        treeview.delete(item)
    
    conn = database.get_connection() [cite: 2]
    if conn:
        try:
            cursor = conn.cursor()
            # Tìm kiếm theo tên hoặc số điện thoại
            sql = "SELECT full_name, phone_number, email, address FROM contacts WHERE full_name LIKE %s OR phone_number LIKE %s"
            params = (f"%{search_query}%", f"%{search_query}%")
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            # chuyển dữ liệu mới vào bảng
            for row in rows:
                treeview.insert("", "end", values=row)
                
        except Exception as e:
            messagebox.showerror("Lỗi tìm kiếm", f"Lỗi: {e}")
        finally:
            conn.close()
