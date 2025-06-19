import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import json

class ModernEntry(tk.Frame):
    def __init__(self, parent, label_text, show=None):
        super().__init__(parent, bg="#f1f5f9")
        self.label = tk.Label(self, text=label_text, font=("Segoe UI", 10), bg="#f1f5f9", fg="#555555")
        self.label.pack(anchor="w", pady=(0, 5))
        self.entry = tk.Entry(self, font=("Segoe UI", 12), bg="#ffffff", fg="#333333", relief="flat", show=show,
                              highlightthickness=1, highlightbackground="#cccccc", highlightcolor="#00BCD4")
        self.entry.pack(fill="x", ipady=8, padx=4)

    def get_value(self):
        return self.entry.get()

def create_manual_attendance_window(parent, token, admin_id):
    attendance_window = tk.Toplevel(parent)
    attendance_window.title("Manual Attendance")
    attendance_window.geometry("800x620")
    attendance_window.configure(bg="#e0f7fa")

    if parent:
        attendance_window.transient(parent)
        attendance_window.grab_set()

    main_frame = tk.Frame(attendance_window, bg="#ffffff", padx=40, pady=30, bd=2, relief="groove")
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = tk.Label(main_frame, text="📋 Manual Attendance Entry", font=("Segoe UI", 22, "bold"),
                           bg="#ffffff", fg="#00796B")
    title_label.pack(pady=(0, 25))

    form_frame = tk.Frame(main_frame, bg="#ffffff")
    form_frame.pack(fill="x", pady=10)

    roll_entry = ModernEntry(form_frame, "🎓 Roll Number")
    roll_entry.pack(fill="x", pady=10)

    date_label = tk.Label(form_frame, text="📅 Date", font=("Segoe UI", 10), bg="#ffffff", fg="#555555")
    date_label.pack(anchor="w")
    date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
    date_entry = tk.Entry(form_frame, textvariable=date_var, font=("Segoe UI", 12),
                          bg="#ffffff", highlightthickness=1, highlightbackground="#cccccc",
                          highlightcolor="#00BCD4", relief="flat")
    date_entry.pack(fill="x", ipady=8, padx=4, pady=(5, 10))

    time_label = tk.Label(form_frame, text="⏰ Time", font=("Segoe UI", 10), bg="#ffffff", fg="#555555")
    time_label.pack(anchor="w")
    time_var = tk.StringVar(value=datetime.now().strftime("%H:%M"))
    time_entry = tk.Entry(form_frame, textvariable=time_var, font=("Segoe UI", 12),
                          bg="#ffffff", highlightthickness=1, highlightbackground="#cccccc",
                          highlightcolor="#00BCD4", relief="flat")
    time_entry.pack(fill="x", ipady=8, padx=4, pady=(5, 10))

    status_frame = tk.Frame(form_frame, bg="#ffffff")
    status_frame.pack(fill="x", pady=20)
    tk.Label(status_frame, text="Mark Attendance", font=("Segoe UI", 12, "bold"),
             bg="#ffffff", fg="#333333").pack(anchor="w", pady=(0, 10))

    buttons_frame = tk.Frame(status_frame, bg="#ffffff")
    buttons_frame.pack()

    status_var = tk.StringVar(value="PRESENT")

    def set_status(status):
        status_var.set(status)
        present_btn.config(bg="#4CAF50" if status == "PRESENT" else "#ffffff", fg="#ffffff" if status == "PRESENT" else "#4CAF50")
        absent_btn.config(bg="#f44336" if status == "ABSENT" else "#ffffff", fg="#ffffff" if status == "ABSENT" else "#f44336")

    present_btn = tk.Button(buttons_frame, text="✓ Present", font=("Segoe UI", 12, "bold"),
                            command=lambda: set_status("PRESENT"),
                            width=12, bg="#4CAF50", fg="white", relief="flat", bd=0, cursor="hand2")
    present_btn.pack(side="left", padx=10)

    absent_btn = tk.Button(buttons_frame, text="✗ Absent", font=("Segoe UI", 12, "bold"),
                           command=lambda: set_status("ABSENT"),
                           width=12, bg="#ffffff", fg="#f44336", relief="flat", bd=0, cursor="hand2")
    absent_btn.pack(side="left", padx=10)

    separator = tk.Frame(main_frame, height=2, bg="#e0e0e0")
    separator.pack(fill="x", pady=20)

    status_message = tk.Label(main_frame, text="", font=("Segoe UI", 11), bg="#fefefe",
                              wraplength=600, justify="center", fg="#444", relief="solid",
                              bd=1, padx=10, pady=8)
    status_message.pack(pady=10, fill="x", padx=20)

    button_frame = tk.Frame(main_frame, bg="#ffffff")
    button_frame.pack(pady=25)

    submit_btn = tk.Button(button_frame, text="✔ Submit Attendance",
                           bg="#00BCD4", fg="white", font=("Segoe UI", 14, "bold"),
                           padx=30, pady=12, bd=0, relief="flat", cursor="hand2")
    submit_btn.pack()

    submit_btn.bind("<Enter>", lambda e: submit_btn.config(bg="#0097A7"))
    submit_btn.bind("<Leave>", lambda e: submit_btn.config(bg="#00BCD4"))

    def submit_attendance():
        try:
            roll_no = roll_entry.get_value().strip()
            if not roll_no:
                status_message.config(text="Please enter a roll number", fg="#f44336")
                return

            try:
                datetime.strptime(date_var.get(), "%Y-%m-%d")
                datetime.strptime(time_var.get(), "%H:%M")
            except ValueError:
                status_message.config(text="Invalid date or time format", fg="#f44336")
                return

            payload = {
                "userId": int(roll_no),
                "status": status_var.get().upper(),
                "role": "ADMIN",
                "marker_id": admin_id
            }

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            response = requests.post(
                "http://localhost:8080/api/attendance/admin/mark",
                headers=headers,
                data=json.dumps(payload)
            )

            if response.status_code == 200:
                messagebox.showinfo("Success", "Attendance recorded successfully")
                roll_entry.entry.delete(0, tk.END)
                status_message.config(text="✔ Attendance recorded successfully", fg="#4CAF50")
            elif response.status_code == 401:
                status_message.config(text="Authentication failed. Please login again.", fg="#f44336")
            elif response.status_code == 404:
                status_message.config(text="Student not found with given roll number", fg="#f44336")
            else:
                status_message.config(text=f"Error: {response.text}", fg="#f44336")

        except Exception as e:
            status_message.config(text=f"Error: {str(e)}", fg="#f44336")

    submit_btn.config(command=submit_attendance)
    return attendance_window
