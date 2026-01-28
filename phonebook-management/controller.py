import tkinter as tk
from tkinter import messagebox
import re

import database 

def validate_data(name, phone):
    if not name.strip():
        messagebox.showerror("Lỗi", "Tên liên hệ không được để trống!")
        return False
    if not phone.isdigit():
        messagebox.showerror("Lỗi", "Số điện thoại chỉ được chứa các chữ số!")
        return False
    if len(phone) < 10 or len(phone) > 11:
        messagebox.showerror("Lỗi", "Số điện thoại phải có từ 10-11 chữ số!")
        return False
    return True
def save_contact_action(name_entry, phone_entry, email_entry, address_text, window):
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_text.get("1.0", "end-1c")
    if validate_data(name, phone):
        conn = database.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
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
    query = search_entry.get().lower()
    pass
