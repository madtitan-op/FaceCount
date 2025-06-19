import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import json
import re

# Custom ModernEntry with placeholder support
class ModernEntry(tk.Frame):
    def __init__(self, parent, placeholder="", show=None, width_chars=None):
        super().__init__(parent, bg="#f9fafb")
        self.placeholder = placeholder
        self.entry = tk.Entry(
            self,
            font=("Segoe UI", 11),
            bg="#ffffff",
            fg="#333333",
            bd=0,
            relief=tk.FLAT,
            show=show,
            width=width_chars
        )
        self.entry.pack(fill=tk.X, ipady=8, padx=10)
        self.configure(highlightbackground="#e0e0e0", highlightcolor="#4CAF50", highlightthickness=1)
        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.config(fg="#999999")

            def on_focus_in(e):
                if self.entry.get() == self.placeholder:
                    self.entry.delete(0, tk.END)
                    self.entry.config(fg="#333333")

            def on_focus_out(e):
                if not self.entry.get():
                    self.entry.insert(0, self.placeholder)
                    self.entry.config(fg="#999999")

            self.entry.bind("<FocusIn>", on_focus_in)
            self.entry.bind("<FocusOut>", on_focus_out)

    def get_value(self):
        return self.entry.get()


# Validation functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_faculty_id(faculty_id):
    if not faculty_id:
        return False, "Faculty ID is required!"
    if not faculty_id.isdigit():
        return False, "Faculty ID must contain only numbers!"
    return True, ""

def validate_name(name):
    if not name:
        return False, "Name is required!"
    if len(name) < 3:
        return False, "Name must be at least 3 characters long!"
    if not all(x.isalpha() or x.isspace() for x in name):
        return False, "Name can only contain letters and spaces!"
    return True, ""

def validate_department(dept):
    if dept == "Select Department":
        return False, "Please select a department!"
    return True, ""

def validate_password(password):
    if not password:
        return False, "Password is required!"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long!"
    return True, ""

def validate_all_inputs(data):
    valid, message = validate_faculty_id(data['faculty_id'])
    if not valid:
        return False, message
    valid, message = validate_name(data['name'])
    if not valid:
        return False, message
    valid, message = validate_department(data['department'])
    if not valid:
        return False, message
    if not validate_email(data['email']):
        return False, "Please enter a valid email address!"
    valid, message = validate_password(data['password'])
    if not valid:
        return False, message
    return True, ""


# Main Admin Register Window class
class AdminRegisterWindow:
    def __init__(self, parent, token):
        self.register_window = tk.Toplevel(parent)
        self.register_window.title("Register New Admin")
        self.register_window.geometry("1000x900")
        self.register_window.configure(bg="#f1f5f9")
        self.register_window.resizable(True, True)
        self.register_window.minsize(1000, 700)
        self.register_window.transient(parent)
        self.register_window.grab_set()

        self.main_container = tk.Frame(self.register_window, bg="#f1f5f9")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        self.form_column = tk.Frame(self.main_container, bg="#ffffff", bd=1, relief=tk.SOLID)
        self.form_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=60, pady=20)

        tk.Label(self.form_column, text="Welcome", font=("Segoe UI", 32, "bold"),
                 fg="#4CAF50", bg="#ffffff").pack(anchor=tk.W, padx=30, pady=(30, 0))
        tk.Label(self.form_column, text="Register new admin account", font=("Segoe UI", 14),
                 fg="#666666", bg="#ffffff").pack(anchor=tk.W, padx=30, pady=(0, 30))

        self.form_frame = tk.Frame(self.form_column, bg="#ffffff")
        self.form_frame.pack(fill=tk.X, pady=10, padx=30, expand=True)

        # ID and Name Row
        row = tk.Frame(self.form_frame, bg="#ffffff")
        row.pack(fill=tk.X, pady=(0, 15))
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=1)

        # Faculty ID
        self.faculty_id = ModernEntry(row, "", width_chars=30)
        tk.Label(row, text="Faculty ID", font=("Segoe UI", 10), bg="#ffffff", fg="#666666").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.faculty_id.grid(row=1, column=0, sticky="ew", padx=(0, 10))

        # Full Name
        self.name = ModernEntry(row, "", width_chars=30)
        tk.Label(row, text="Full Name", font=("Segoe UI", 10), bg="#ffffff", fg="#666666").grid(row=0, column=1, sticky="w", pady=(0, 5))
        self.name.grid(row=1, column=1, sticky="ew")

        # Department Dropdown
        departments = ["CSE", "ECE", "EE", "ME", "CE"]
        self.department_var = tk.StringVar(value='Select Department')
        tk.Label(self.form_frame, text="Department", font=("Segoe UI", 10),
                 bg="#ffffff", fg="#666666").pack(anchor="w", pady=(0, 5))
        self.department_menu = ttk.Combobox(self.form_frame, textvariable=self.department_var,
                                            values=departments, width=27, state='readonly')
        self.department_menu.pack(fill=tk.X, pady=(0, 15))

        # Role Dropdown
        roles = ["FACULTY", "ADMIN"]
        self.role_var = tk.StringVar(value='FACULTY')
        tk.Label(self.form_frame, text="Role", font=("Segoe UI", 10),
                 bg="#ffffff", fg="#666666").pack(anchor="w", pady=(0, 5))
        self.role_menu = ttk.Combobox(self.form_frame, textvariable=self.role_var,
                                      values=roles, width=27, state='readonly')
        self.role_menu.pack(fill=tk.X, pady=(0, 15))

        # Email
        tk.Label(self.form_frame, text="Email", font=("Segoe UI", 10),
                 bg="#ffffff", fg="#666666").pack(anchor="w", pady=(0, 5))
        self.email = ModernEntry(self.form_frame, "Enter your email", width_chars=60)
        self.email.pack(fill=tk.X, pady=(0, 15))

        # Password
        tk.Label(self.form_frame, text="Password", font=("Segoe UI", 10),
                 bg="#ffffff", fg="#666666").pack(anchor="w", pady=(0, 5))
        self.password = ModernEntry(self.form_frame, "", show="●", width_chars=60)
        self.password.pack(fill=tk.X, pady=(0, 15))

        self.error_label = tk.Label(self.form_frame, text="", font=("Segoe UI", 10),
                                    fg="#FF4444", bg="#ffffff")
        self.error_label.pack(pady=(0, 10))

        # Register Button
        self.submit_btn = tk.Button(self.form_frame, text="Register Admin", font=("Segoe UI", 12, "bold"),
                                    bg="#4CAF50", fg="white", padx=30, pady=12, bd=0, cursor="hand2",
                                    relief=tk.FLAT, command=self.register_admin)
        self.submit_btn.pack(pady=20)
        self.submit_btn.bind('<Enter>', lambda e: self.submit_btn.config(bg="#45a049"))
        self.submit_btn.bind('<Leave>', lambda e: self.submit_btn.config(bg="#4CAF50"))

        self.token = token

        def on_closing():
            self.register_window.grab_release()
            self.register_window.destroy()

        self.register_window.protocol("WM_DELETE_WINDOW", on_closing)

    def register_admin(self):
        try:
            data = {
                'faculty_id': self.faculty_id.get_value().strip(),
                'name': self.name.get_value().strip(),
                'email': self.email.get_value().strip(),
                'password': self.password.get_value(),
                'department': self.department_var.get(),
                'role': self.role_var.get()
            }

            valid, message = validate_all_inputs(data)
            if not valid:
                self.error_label.config(text=message)
                return

            server_data = {
                'faculty_id': int(data['faculty_id']),
                'name': data['name'],
                'email': data['email'],
                'password': data['password'],
                'department': data['department'],
                'role': data['role']
            }

            response = requests.post(
                "http://localhost:8080/api/faculty/admin/register",
                data=json.dumps(server_data),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.token}'
                }
            )

            if response.status_code == 200:
                messagebox.showinfo("Success", "Admin registered successfully!")
                self.register_window.destroy()
            elif response.status_code == 401:
                self.error_label.config(text="Authentication failed. Please login again.")
            elif response.status_code == 409:
                self.error_label.config(text="Faculty ID or email already exists")
            else:
                self.error_label.config(text=f"Error: {response.text or 'Unknown error occurred'}")

        except requests.exceptions.RequestException as e:
            self.error_label.config(text=f"Network error: {str(e)}")
        except Exception as e:
            self.error_label.config(text=f"Error: {str(e)}")

# Create window function
def create_admin_register_window(parent, token):
    return AdminRegisterWindow(parent, token).register_window

# Prevent direct run
if __name__ == "__main__":
    root = tk.Tk()
    messagebox.showerror("Error", "This file should not be run directly. Please run the main application.")
    root.destroy()
