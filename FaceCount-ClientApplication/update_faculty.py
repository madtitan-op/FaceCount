import tkinter as tk
from tkinter import ttk, messagebox
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

def create_faculty_modify_window(parent, token):
    # Create the main window
    window = tk.Toplevel(parent)
    window.title("🛠 Modify Faculty Details")
    window.geometry("800x600")
    window.configure(bg="#E8F0FE")
    window.transient(parent)
    window.grab_set()

    # Create the main container
    main_container = tk.Frame(window, bg="#E8F0FE")
    main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Header
    header = tk.Label(main_container, text="Update Faculty Profile", 
                     font=("Helvetica", 20, "bold"), 
                     bg="#E8F0FE", fg="#1a73e8")
    header.pack(pady=(0, 10))

    # Create the form frame
    form_frame = tk.Frame(main_container, bg="#ffffff", 
                         highlightbackground="#cfcfcf", 
                         highlightthickness=1)
    form_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    # Search section
    search_frame = tk.Frame(form_frame, bg="#ffffff")
    search_frame.pack(fill=tk.X, padx=20, pady=10)

    faculty_id_entry = ModernEntry(search_frame, "🆔 Enter Faculty ID")
    faculty_id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

    # Status label for messages
    status_label = tk.Label(form_frame, text="", font=("Helvetica", 9), 
                           bg="#ffffff", fg="#f44336")
    status_label.pack(pady=5)

    # Fields dictionary to store all input fields
    fields = {}

    # Details section
    details_frame = tk.Frame(form_frame, bg="#ffffff")
    details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Name field
    fields['name'] = ModernEntry(details_frame, "🧑 Name")
    fields['name'].pack(fill=tk.X, pady=5)

    # Email field
    fields['email'] = ModernEntry(details_frame, "📧 Email")
    fields['email'].pack(fill=tk.X, pady=5)

    # Department dropdown
    dept_frame = tk.Frame(details_frame, bg="#ffffff")
    dept_frame.pack(fill=tk.X, pady=5)
    tk.Label(dept_frame, text="🏫 Department", 
            font=("Helvetica", 9, "bold"), 
            bg="#ffffff", fg="#4A4A4A").pack(anchor=tk.W)
    dept_var = tk.StringVar(value="Select Department")
    fields['department'] = dept_var
    dept_menu = ttk.OptionMenu(dept_frame, dept_var, "Select Department", 
                              *["CSE", "ECE", "EE", "ME", "CE"])
    dept_menu.config(width=35)
    dept_menu.pack(fill=tk.X, pady=2)

    # Role dropdown
    role_frame = tk.Frame(details_frame, bg="#ffffff")
    role_frame.pack(fill=tk.X, pady=5)
    tk.Label(role_frame, text="🧑‍🏫 Role", 
            font=("Helvetica", 9, "bold"), 
            bg="#ffffff", fg="#4A4A4A").pack(anchor=tk.W)
    role_var = tk.StringVar(value="Select Role")
    fields['role'] = role_var
    role_menu = ttk.OptionMenu(role_frame, role_var, "Select Role", 
                              "FACULTY", "ADMIN")
    role_menu.config(width=35)
    role_menu.pack(fill=tk.X, pady=2)

    # Password field
    fields['password'] = ModernEntry(details_frame, "🔒 Password", show="*")
    fields['password'].pack(fill=tk.X, pady=5)

    def search_faculty():
        faculty_id = faculty_id_entry.get_value().strip()
        if not faculty_id:
            status_label.config(text="Please enter Faculty ID", fg="#f44336")
            return

        try:
            response = requests.get(
                f"http://localhost:8080/api/faculty/admin/details/{faculty_id}",
                headers={'Authorization': f'Bearer {token}'}
            )
            if response.status_code == 200:
                data = response.json()
                fields['name'].set_value(data.get('name', ''))
                fields['email'].set_value(data.get('email', ''))
                dept_var.set(data.get('department', 'Select Department'))
                role_var.set(data.get('role', 'FACULTY'))
                fields['password'].set_value(data.get('password', ''))
                status_label.config(text="✅ Faculty found", fg="#4CAF50")
            elif response.status_code == 404:
                status_label.config(text="❌ Faculty not found", fg="#f44336")
            else:
                status_label.config(text="⚠️ Failed to fetch details", fg="#f44336")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}", fg="#f44336")

    # Search button
    search_button = tk.Button(search_frame, text="🔍 Search", 
                            command=search_faculty,
                            bg="#1a73e8", fg="white", 
                            font=("Helvetica", 10, "bold"),
                            relief="flat", padx=15, pady=4, 
                            cursor="hand2")
    search_button.pack(side=tk.RIGHT)

    def update_faculty():
        faculty_id = faculty_id_entry.get_value().strip()
        if not faculty_id:
            status_label.config(text="Please enter Faculty ID", fg="#f44336")
            return

        current_values = {
            'faculty_id': int(faculty_id),
            'name': fields['name'].get_value().strip(),
            'email': fields['email'].get_value().strip(),
            'department': fields['department'].get(),
            'password': fields['password'].get_value().strip(),
            'role': fields['role'].get()
        }

        if current_values['department'] == "Select Department":
            status_label.config(text="Please select a department", fg="#f44336")
            return
        if not current_values['name'] or not current_values['email'] or not current_values['password']:
            status_label.config(text="Name, Email, and Password are required", fg="#f44336")
            return
        if current_values['role'] == "Select Role":
            status_label.config(text="Please select a valid Role", fg="#f44336")
            return

        try:
            response = requests.put(
                f"http://localhost:8080/api/faculty/admin/update/{faculty_id}",
                data=json.dumps(current_values),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                }
            )
            if response.status_code == 200:
                messagebox.showinfo("✅ Success", "Faculty details updated successfully")
                window.destroy()
            else:
                status_label.config(text=f"Update failed: {response.status_code}", fg="#f44336")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}", fg="#f44336")

    # Button frame
    button_frame = tk.Frame(form_frame, bg="#ffffff")
    button_frame.pack(pady=15)

    # Update button
    update_button = tk.Button(button_frame, text="✅ Update", 
                            command=update_faculty,
                            bg="#34A853", fg="white", 
                            font=("Helvetica", 11, "bold"),
                            relief="flat", padx=20, pady=6, 
                            cursor="hand2")
    update_button.pack(side=tk.LEFT, padx=5)

    # Cancel button
    cancel_button = tk.Button(button_frame, text="❌ Cancel", 
                            command=window.destroy,
                            bg="#EA4335", fg="white", 
                            font=("Helvetica", 11, "bold"),
                            relief="flat", padx=20, pady=6, 
                            cursor="hand2")
    cancel_button.pack(side=tk.LEFT, padx=5)

    # Make window modal
    window.transient(parent)
    window.grab_set()

    # Handle window closing
    def on_closing():
        window.grab_release()
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    return window
