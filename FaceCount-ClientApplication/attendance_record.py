import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime

def create_attendance_window(parent, token):
    attendance_window = tk.Toplevel(parent)
    attendance_window.title("Attendance Records")
    attendance_window.geometry("1000x600")
    attendance_window.configure(bg="#f4f6f9")

    # Style setup for Treeview
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#ffffff",
                    foreground="#333333",
                    rowheight=30,
                    fieldbackground="#ffffff",
                    font=("Segoe UI", 10))
    style.map("Treeview", background=[("selected", "#cce5ff")])
    style.configure("Treeview.Heading",
                    background="#007acc",
                    foreground="white",
                    font=("Segoe UI", 11, "bold"))

    # Main container
    main_frame = tk.Frame(attendance_window, bg="#f4f6f9", padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)

    # Search frame
    search_frame = tk.Frame(main_frame, bg="#f4f6f9")
    search_frame.pack(fill="x", pady=(0, 20))

    # Date picker label
    date_label = tk.Label(search_frame, text="📅 Select Date:", bg="#f4f6f9", font=("Segoe UI", 10, "bold"))
    date_label.pack(side="left", padx=(0, 10))

    # Date Entry
    date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
    date_entry_container = tk.Frame(search_frame, bg="#e9ecef", bd=1, relief="flat")
    date_entry_container.pack(side="left", padx=(0, 20))
    date_entry = tk.Entry(date_entry_container, textvariable=date_var, font=("Segoe UI", 10),
                          bg="#e9ecef", bd=0, relief="flat", width=15)
    date_entry.pack(ipady=6, padx=10)

    # Fetch button
    def on_enter(e):
        fetch_btn.config(bg="#005bb5")

    def on_leave(e):
        fetch_btn.config(bg="#007acc")

    fetch_btn = tk.Button(search_frame, text="🔍 Fetch Records", command=lambda: fetch_attendance(),
                          bg="#007acc", fg="white", font=("Segoe UI", 10, "bold"),
                          relief="flat", padx=20, pady=6, cursor="hand2")
    fetch_btn.pack(side="left")
    fetch_btn.bind("<Enter>", on_enter)
    fetch_btn.bind("<Leave>", on_leave)

    # Treeview Frame
    tree_frame = tk.Frame(main_frame, bg="#f4f6f9")
    tree_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=("Roll No", "Date", "Status"), show="headings")
    tree.heading("Roll No", text="Roll No")
    tree.heading("Date", text="Date")
    tree.heading("Status", text="Status")
    tree.column("Roll No", width=200, anchor="center")
    tree.column("Date", width=200, anchor="center")
    tree.column("Status", width=150, anchor="center")

    # Scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(fill="both", expand=True)

    # Attendance fetching logic
    def fetch_attendance():
        tree.delete(*tree.get_children())  # Clear existing
        date_str = date_var.get()
        try:
            dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day, month, year = dt_obj.day, dt_obj.month, dt_obj.year
        except ValueError:
            messagebox.showerror("Invalid Date", "Invalid date format. Please use YYYY-MM-DD.")
            return

        try:
            response = requests.get(
                f"http://localhost:8080/api/attendance/fetch/{day}/{month}/{year}",
                headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                records = response.json()
                if isinstance(records, list):
                    for record in records:
                        if isinstance(record, dict):
                            roll_no = record.get("userId", "")
                            if not roll_no:
                                continue
                            date = record.get("date", "")
                            status = record.get("status", "")
                            tree.insert("", "end", values=(roll_no, date, status))
                else:
                    messagebox.showinfo("No Records", "No attendance records found for this date.")
            else:
                messagebox.showerror("Fetch Error", f"Error fetching attendance: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")

    return attendance_window
