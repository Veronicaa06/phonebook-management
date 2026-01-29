import tkinter as tk
from tkinter import messagebox
import sqlite3 
import database 

def validate_data(name, phone):
    if not name.strip():
        messagebox.showerror("Error", "Contact name cannot be left blank!")
        return False
    if not phone.isdigit():
        messagebox.showerror("Error", "Phone number must contain only digits!")
        return False
    
    if len(phone) < 10 or len(phone) > 11:
        messagebox.showerror("Error", "Phone number must have between 10-11 digits!")
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
                sql = "INSERT INTO contacts (full_name, phone_number, email, address) VALUES (?, ?, ?, ?)"
                val = (name, phone, email, address)
                cursor.execute(sql, val)
                conn.commit()
                messagebox.showinfo("Success", "Successfully added new contact to SQLite!")
                window.destroy()  
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to save: {e}")
            finally:
                conn.close()

def search_contact_logic(search_entry, treeview):
    search_query = search_entry.get().strip()
    for item in treeview.get_children():
        treeview.delete(item)
    
    conn = database.get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "SELECT full_name, phone_number, email, address FROM contacts WHERE full_name LIKE ? OR phone_number LIKE ?"
            params = (f"%{search_query}%", f"%{search_query}%")
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            for row in rows:
                treeview.insert("", "end", values=row)
                
        except Exception as e:
            messagebox.showerror("Search Error", f"Error: {e}")
        finally:
            conn.close()
