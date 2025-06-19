import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests
import json

class ModernEntry(tk.Frame):
    def __init__(self, parent, label_text, show=None):
        super().__init__(parent, bg="#ffffff")
        self.label = tk.Label(self, text=label_text, font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#4A4A4A")
        self.label.pack(anchor="w", pady=(0, 2))

        self.entry = tk.Entry(self, font=("Helvetica", 12), bg="#F1F3F4", fg="#202124", relief="flat", show=show)
        self.entry.pack(fill="x", ipady=6)

        self.border = tk.Frame(self, height=2, bg="#C1C1C1")
        self.border.pack(fill="x", pady=(2, 10))

    def get_value(self):
        return self.entry.get()

    def set_value(self, value):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(value) if value is not None else '')

def create_modify_window(parent, token):
    modify_window = tk.Toplevel(parent)
    modify_window.title("🛠 Modify Student Details")
    modify_window.geometry("1200x800")
    modify_window.configure(bg="#E8F0FE")

    if parent:
        modify_window.transient(parent)
        modify_window.grab_set()

    heading = tk.Label(modify_window, text="Modify Student Profile", font=("Helvetica", 20, "bold"), bg="#E8F0FE", fg="#1a73e8")
    heading.pack(pady=20)

    main_frame = tk.Frame(modify_window, bg="#ffffff", padx=40, pady=30, highlightbackground="#cfcfcf", highlightthickness=1)
    main_frame.pack(fill="both", expand=True, padx=60, pady=20)

    search_frame = tk.Frame(main_frame, bg="#ffffff")
    search_frame.pack(fill="x", pady=(0, 20))

    roll_entry = ModernEntry(search_frame, "🎓 Enter Roll Number")
    roll_entry.pack(side="left", expand=True, padx=(0, 10))

    search_button = tk.Button(search_frame, text="🔍 Search", command=lambda: search_user(),
                              bg="#1a73e8", fg="white", font=("Helvetica", 11, "bold"),
                              relief="flat", padx=20, pady=6, cursor="hand2", activebackground="#155ab6")
    search_button.pack(side="right", pady=10)

    fields = {}

    details_frame = tk.Frame(main_frame, bg="#ffffff")
    details_frame.pack(fill="both", expand=True)

    left_frame = tk.Frame(details_frame, bg="#ffffff")
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

    right_frame = tk.Frame(details_frame, bg="#ffffff")
    right_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

    fields['name'] = ModernEntry(left_frame, "🧑 Full Name")
    fields['name'].pack(fill="x", pady=10)

    fields['email'] = ModernEntry(left_frame, "📧 Email Address")
    fields['email'].pack(fill="x", pady=10)

    dept_frame = tk.Frame(left_frame, bg="#ffffff")
    dept_frame.pack(fill="x", pady=10)
    tk.Label(dept_frame, text="🏫 Department", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#4A4A4A").pack(anchor="w", pady=(0, 2))
    dept_var = tk.StringVar(value="Select Department")
    fields['department'] = dept_var
    dept_menu = ttk.OptionMenu(dept_frame, dept_var, "Select Department", *["CSE", "ECE", "EE", "ME", "CE"])
    dept_menu.pack(fill="x", ipady=4)

    yop_frame = tk.Frame(right_frame, bg="#ffffff")
    yop_frame.pack(fill="x", pady=10)
    tk.Label(yop_frame, text="📅 Year of Passing", font=("Helvetica", 10, "bold"), bg="#ffffff", fg="#4A4A4A").pack(anchor="w", pady=(0, 2))
    yop_var = tk.StringVar(value="Select Year")
    fields['yop'] = yop_var
    current_year = datetime.now().year
    yop_menu = ttk.OptionMenu(yop_frame, yop_var, "Select Year", *list(range(current_year, current_year + 6)))
    yop_menu.pack(fill="x", ipady=4)

    fields['password'] = ModernEntry(right_frame, "🔒 Password", show="*")
    fields['password'].pack(fill="x", pady=10)

    status_label = tk.Label(main_frame, text="", font=("Helvetica", 10), bg="#ffffff", fg="#f44336")
    status_label.pack(pady=10)

    original_data = {}

    def search_user():
        rollno = roll_entry.get_value().strip()
        if not rollno:
            status_label.config(text="Please enter a roll number", fg="#f44336")
            return
        try:
            response = requests.get(
                f"http://localhost:8080/api/student/admin/details/{rollno}",
                headers={'Authorization': f'Bearer {token}'}
            )
            if response.status_code == 200:
                user = response.json()
                original_data.clear()
                original_data.update(user)
                fields['name'].set_value(user.get('name', ''))
                fields['email'].set_value(user.get('email', ''))
                fields['department'].set(user.get('department', 'Select Department'))
                fields['yop'].set(str(user.get('yop', 'Select Year')))
                fields['password'].set_value(user.get('password', ''))
                status_label.config(text="✅ User found successfully", fg="#4CAF50")
            elif response.status_code == 404:
                status_label.config(text="❌ User not found", fg="#f44336")
            elif response.status_code == 401:
                status_label.config(text="⚠️ Authentication failed", fg="#f44336")
            else:
                status_label.config(text="⚠️ Unexpected error occurred", fg="#f44336")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}", fg="#f44336")

    def update_user():
        student_id = roll_entry.get_value().strip()
        if not student_id:
            status_label.config(text="Please enter a roll number", fg="#f44336")
            return

        current_values = {
            'name': fields['name'].get_value().strip(),
            'email': fields['email'].get_value().strip(),
            'department': fields['department'].get(),
            'yop': fields['yop'].get(),
            'password': fields['password'].get_value()
        }

        if current_values['department'] == "Select Department":
            status_label.config(text="Please select a valid Department", fg="#f44336")
            return
        if current_values['yop'] == "Select Year":
            status_label.config(text="Please select a valid Year of Passing", fg="#f44336")
            return
        if not current_values['name'] or not current_values['email'] or not current_values['password']:
            status_label.config(text="Name, Email, and Password are required", fg="#f44336")
            return

        try:
            update_data = {
                'student_id': int(student_id),
                'role': 'STUDENT',
                'name': current_values['name'],
                'email': current_values['email'],
                'department': current_values['department'],
                'yop': int(current_values['yop']),
                'password': current_values['password']
            }
        except ValueError:
            status_label.config(text="Year of Passing must be a number", fg="#f44336")
            return

        try:
            response = requests.put(
                f"http://localhost:8080/api/student/admin/update/{student_id}",
                data=json.dumps(update_data),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                }
            )
            if response.status_code == 200:
                messagebox.showinfo("✅ Success", "User details updated successfully")
                modify_window.destroy()
            else:
                status_label.config(text=f"Update failed: {response.status_code}", fg="#f44336")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}", fg="#f44336")

    # Buttons
    button_frame = tk.Frame(main_frame, bg="#ffffff")
    button_frame.pack(pady=30)

    update_button = tk.Button(button_frame, text="✅ Update", command=update_user,
                              bg="#34A853", fg="white", font=("Helvetica", 12, "bold"),
                              relief="flat", padx=25, pady=8, cursor="hand2", activebackground="#2c8b45")
    update_button.pack(side="left", padx=10)

    cancel_button = tk.Button(button_frame, text="❌ Cancel", command=modify_window.destroy,
                              bg="#EA4335", fg="white", font=("Helvetica", 12, "bold"),
                              relief="flat", padx=25, pady=8, cursor="hand2", activebackground="#c72c1d")
    cancel_button.pack(side="left", padx=10)

    return modify_window
