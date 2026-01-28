import tkinter as tk

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

# Gán popup cho nút Add Contact
btn_add.config(command=open_add_contact)

# ================== RUN ==================
root.mainloop()

