import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import re

# Custom modern entry widget
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
            self.entry.bind('<FocusIn>', self._clear_placeholder)
            self.entry.bind('<FocusOut>', self._add_placeholder)
            self.entry.config(fg='#666666')

    def _clear_placeholder(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg='#333333')

    def _add_placeholder(self, event):
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg='#666666')

    def get(self):
        text = self.entry.get()
        return "" if text == self.placeholder else text

# Validation functions
def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, ""

# Main System Register Window class
class SystemRegisterWindow:
    def __init__(self, parent, token):
        self.register_window = tk.Toplevel(parent)
        self.register_window.title("Register New System")
        self.register_window.geometry("800x500")
        self.register_window.configure(bg="#f1f5f9")
        self.register_window.resizable(True, True)
        self.register_window.minsize(800, 500)
        self.register_window.transient(parent)
        self.register_window.grab_set()

        self.main_container = tk.Frame(self.register_window, bg="#f1f5f9")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.form_column = tk.Frame(self.main_container, bg="#ffffff", bd=1, relief=tk.SOLID)
        self.form_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=15)

        tk.Label(self.form_column, text="Welcome", font=("Segoe UI", 24, "bold"),
                fg="#4CAF50", bg="#ffffff").pack(anchor=tk.W, padx=20, pady=(20, 0))
        tk.Label(self.form_column, text="Register new system", font=("Segoe UI", 12),
                fg="#666666", bg="#ffffff").pack(anchor=tk.W, padx=20, pady=(0, 20))

        self.form_frame = tk.Frame(self.form_column, bg="#ffffff")
        self.form_frame.pack(fill=tk.X, pady=10, padx=20, expand=True)

        # System ID
        tk.Label(self.form_frame, text="System ID", font=("Segoe UI", 10),
                bg="#ffffff", fg="#666666").pack(anchor="w", pady=(0, 5))
        self.system_id = ModernEntry(self.form_frame, "", width_chars=60)
        self.system_id.pack(fill=tk.X, pady=(0, 15))

        # Department Dropdown
        departments = ["CSE", "ECE", "EE", "ME", "CE"]
        self.department_var = tk.StringVar(value='Select Department')
        tk.Label(self.form_frame, text="Department", font=("Segoe UI", 10),
                bg="#ffffff", fg="#666666").pack(anchor="w", pady=(0, 5))
        self.department_menu = ttk.Combobox(self.form_frame, textvariable=self.department_var,
                                          values=departments, width=27, state='readonly')
        self.department_menu.pack(fill=tk.X, pady=(0, 15))

        # Password
        tk.Label(self.form_frame, text="Password", font=("Segoe UI", 10),
                bg="#ffffff", fg="#666666").pack(anchor="w", pady=(0, 5))
        self.password = ModernEntry(self.form_frame, "", show="●", width_chars=60)
        self.password.pack(fill=tk.X, pady=(0, 15))

        self.error_label = tk.Label(self.form_frame, text="", font=("Segoe UI", 10),
                                  fg="#FF4444", bg="#ffffff")
        self.error_label.pack(pady=(0, 10))

        # Register Button
        self.submit_btn = tk.Button(self.form_frame, text="Register System", font=("Segoe UI", 11, "bold"),
                                  bg="#4CAF50", fg="white", padx=20, pady=8, bd=0, cursor="hand2",
                                  relief=tk.FLAT, command=self.register_system)
        self.submit_btn.pack(pady=15)
        self.submit_btn.bind('<Enter>', lambda e: self.submit_btn.config(bg="#45a049"))
        self.submit_btn.bind('<Leave>', lambda e: self.submit_btn.config(bg="#4CAF50"))

        self.token = token

        def on_closing():
            self.register_window.grab_release()
            self.register_window.destroy()

        self.register_window.protocol("WM_DELETE_WINDOW", on_closing)

    def validate_system_id(self, system_id):
        if not system_id:
            return False, "System ID is required!"
        if not system_id.isdigit():
            return False, "System ID must contain only numbers!"
        return True, ""

    def register_system(self):
        try:
            # Validate inputs
            system_id = self.system_id.get().strip()
            department = self.department_var.get()
            password = self.password.get()

            # Validate system ID
            is_valid, error_msg = self.validate_system_id(system_id)
            if not is_valid:
                self.error_label.config(text=error_msg)
                return

            if department == 'Select Department':
                self.error_label.config(text="Please select a department")
                return

            is_valid, error_msg = validate_password(password)
            if not is_valid:
                self.error_label.config(text=error_msg)
                return

            data = {
                "system_id": int(system_id),  # Convert to integer
                "department": department,
                "password": password,
                "role": "SYSTEM"
            }

            # Print request data for debugging
            print("Sending request with data:", data)
            print("Token:", self.token)

            try:
                response = requests.post(
                    'http://localhost:8080/api/system/create',
                    data=json.dumps(data),
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {self.token}',
                        'Accept': 'application/json',
                        'Origin': 'http://localhost:8080'
                    }
                )
                
                # Print response for debugging
                print("Response status:", response.status_code)
                print("Response headers:", response.headers)
                print("Response content:", response.text)

                if response.status_code in [200, 201]:  # Accept both 200 and 201 as success
                    try:
                        response_data = response.json()
                        # Create a formatted message with the response data
                        message = "System registered successfully!\n\n"
                        message += "System Details:\n"
                        message += f"System ID: {response_data.get('system_id', 'N/A')}\n"
                        message += f"Department: {response_data.get('department', 'N/A')}\n"
                       
                        
                        # Show the detailed message in a popup
                        messagebox.showinfo("Registration Success", message)
                        self.register_window.destroy()
                    except json.JSONDecodeError:
                        self.error_label.config(text="Error: Invalid response from server")
                else:
                    error_message = "Error: "
                    try:
                        error_data = response.json()
                        error_message += error_data.get('detail', response.text)
                    except:
                        error_message += response.text or 'Unknown error occurred'
                    self.error_label.config(text=error_message)

            except requests.exceptions.ConnectionError:
                self.error_label.config(text="Error: Could not connect to server. Please check if the server is running.")
            except requests.exceptions.RequestException as e:
                self.error_label.config(text=f"Network error: {str(e)}")

        except Exception as e:
            self.error_label.config(text=f"Error: {str(e)}")
            print("Full error:", str(e))  # Print full error for debugging

def create_system_register_window(parent, token):
    return SystemRegisterWindow(parent, token).register_window