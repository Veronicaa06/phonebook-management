import tkinter as tk
from tkinter import ttk, messagebox
import controller
import database


# ================== MAIN WINDOW ==================
root = tk.Tk()
root.title("Phone Book Management System")
root.geometry("1100x650")
root.configure(bg="#1E1E2F")

# ================== HEADER ==================
header_frame = tk.Frame(root, bg="#4A90E2", height=60)
header_frame.pack(fill="x")

lbl_title = tk.Label(
    header_frame,
    text="PHONE BOOK MANAGEMENT SYSTEM",
    bg="#4A90E2",
    fg="white",
    font=("Arial", 16, "bold")
)
lbl_title.pack(pady=15)

# ================== BODY ==================
body_frame = tk.Frame(root)
body_frame.pack(fill="both", expand=True)

# ================== LEFT MENU ==================
menu_frame = tk.Frame(body_frame, bg="#F4F6F8", width=250)
menu_frame.pack(side="left", fill="y")
menu_frame.pack_propagate(False)

menu_inner = tk.Frame(menu_frame, bg="#F4F6F8")
menu_inner.place(relx=0.5, rely=0.5, anchor="center")

menu_font = ("Arial", 11)

def create_menu_button(text):
    btn = tk.Button(
        menu_inner,
        text=text,
        width=22,
        height=2,
        font=("Arial", 11),
        bg="white",
        fg="#333333",
        relief="solid",
        bd=1,
        cursor="hand2"
    )

    # Hover vào
    def on_enter(e):
        btn.config(
            bg="#E3F2FD",
            fg="#1565C0",
            bd=2
        )

    # Hover ra
    def on_leave(e):
        btn.config(
            bg="white",
            fg="#333333",
            bd=1
        )

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    return btn

btn_view_list = create_menu_button("View Contact List")
btn_search    = create_menu_button("Search Contact")
btn_update    = create_menu_button("Update Contact")
btn_add       = create_menu_button("Add Contact")
btn_delete    = create_menu_button("Delete Contact")
btn_exit      = create_menu_button("Exit System")

for btn in [
    btn_view_list,
    btn_search,
    btn_update,
    btn_add,
    btn_delete,
    btn_exit
]:
    btn.pack(pady=9)

# ================== CONTENT AREA ==================
content_frame = tk.Frame(body_frame, bg="#1E1E2F")
content_frame.pack(side="right", fill="both", expand=True)

def view_contact_list():
    # Xóa nội dung cũ
    for widget in content_frame.winfo_children():
        widget.destroy()

    columns = ("Name", "Phone", "Email", "Address")
    tree = ttk.Treeview(content_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, phone_number, email, address FROM contacts")

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    conn.close()

def search_contact():
    for widget in content_frame.winfo_children():
        widget.destroy()

    top_frame = tk.Frame(content_frame)
    top_frame.pack(pady=10)

    tk.Label(top_frame, text="Search:").pack(side="left", padx=5)
    search_entry = tk.Entry(top_frame, width=30)
    search_entry.pack(side="left", padx=5)

    columns = ("Name", "Phone", "Email", "Address")
    tree = ttk.Treeview(content_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    def do_search():
        controller.search_contact_logic(search_entry, tree)

    tk.Button(top_frame, text="Search", command=do_search).pack(side="left", padx=5)

def delete_contact():
    for widget in content_frame.winfo_children():
        widget.destroy()

    columns = ("ID", "Name", "Phone", "Email", "Address")
    tree = ttk.Treeview(content_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, phone_number, email, address FROM contacts")

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    conn.close()

    def do_delete():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a contact to delete")
            return

        values = tree.item(selected[0])["values"]
        contact_id = values[0]

        if not messagebox.askyesno("Confirm", "Delete this contact?"):
            return

        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Done", "Contact deleted")
        delete_contact()  # reload lại danh sách

    tk.Button(content_frame, text="Delete Selected", command=do_delete)\
        .pack(pady=10)


def update_contact():
    for widget in content_frame.winfo_children():
        widget.destroy()

    columns = ("ID", "Name", "Phone", "Email", "Address")
    tree = ttk.Treeview(content_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, phone_number, email, address FROM contacts")

    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    conn.close()

    def open_update_popup():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a contact to update")
            return

        values = tree.item(selected[0])["values"]
        contact_id = values[0]

        win = tk.Toplevel()
        win.title("Update Contact")
        win.geometry("400x350")

        tk.Label(win, text="Name").pack()
        name_entry = tk.Entry(win)
        name_entry.insert(0, values[1])
        name_entry.pack()

        tk.Label(win, text="Phone").pack()
        phone_entry = tk.Entry(win)
        phone_entry.insert(0, values[2])
        phone_entry.pack()

        tk.Label(win, text="Email").pack()
        email_entry = tk.Entry(win)
        email_entry.insert(0, values[3])
        email_entry.pack()

        tk.Label(win, text="Address").pack()
        address_text = tk.Text(win, height=4)
        address_text.insert("1.0", values[4])
        address_text.pack()

        def save_update():
            conn = database.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE contacts
                SET full_name=?, phone_number=?, email=?, address=?
                WHERE id=?
            """, (
                name_entry.get(),
                phone_entry.get(),
                email_entry.get(),
                address_text.get("1.0", "end-1c"),
                contact_id
            ))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Contact updated")
            win.destroy()
            update_contact()

        tk.Button(win, text="Save", command=save_update).pack(pady=10)

    tk.Button(
        content_frame,
        text="Update Selected",
        command=open_update_popup
    ).pack(pady=10)


# ================== ADD CONTACT POPUP ==================
def open_add_contact():
    add_window = tk.Toplevel(root)
    add_window.title("Add New Contact")
    add_window.geometry("500x420")
    add_window.configure(bg="#F4F6F8")

    lbl_add_title = tk.Label(
        add_window,
        text="Add New Contact",
        bg="#F4F6F8",
        fg="#333333",
        font=("Arial", 15, "bold")
    )
    lbl_add_title.pack(pady=20)

    form_frame = tk.Frame(add_window, bg="#F4F6F8")
    form_frame.pack(pady=10)

    labels = ["Name:", "Phone:", "Email:", "Address:"]
    for i, text in enumerate(labels):
        tk.Label(
            form_frame,
            text=text,
            bg="#F4F6F8",
            fg="#333333",
            font=("Arial", 11)
        ).grid(row=i, column=0, pady=6, sticky="e")

    entry_name = tk.Entry(form_frame, width=30)
    entry_phone = tk.Entry(form_frame, width=30)
    entry_email = tk.Entry(form_frame, width=30)
    txt_address = tk.Text(form_frame, width=30, height=4)

    entry_name.grid(row=0, column=1, pady=6)
    entry_phone.grid(row=1, column=1, pady=6)
    entry_email.grid(row=2, column=1, pady=6)
    txt_address.grid(row=3, column=1, pady=6)

    btn_frame = tk.Frame(add_window, bg="#F4F6F8")
    btn_frame.pack(pady=20)

    btn_save = tk.Button(
        btn_frame, text="Save",
        width=12, height=2,
        bg="#4A90E2", fg="white",
        font=("Arial", 11),
        relief="flat"
    )
    btn_save.config(command=lambda: controller.save_contact_action(
        entry_name, 
        entry_phone, 
        entry_email, 
        txt_address, 
        add_window
    ))
    btn_cancel = tk.Button(
        btn_frame, text="Cancel",
        width=12, height=2,
        bg="#B0BEC5", fg="white",
        font=("Arial", 11),
        relief="flat",
        command=add_window.destroy
    )

    btn_save.pack(side="left", padx=15)
    btn_cancel.pack(side="right", padx=15)


btn_add.config(command=open_add_contact)
btn_view_list.config(command=view_contact_list)
btn_search.config(command=search_contact)
btn_delete.config(command=delete_contact)
btn_update.config(command=update_contact)
btn_exit.config(command=root.destroy)


# ================== RUN ==================
def run_app():
    root.mainloop()


