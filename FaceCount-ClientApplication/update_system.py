import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

from datetime import datetime  # Only needed if you use dates

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

def create_system_update_window(parent, token):
    win = tk.Toplevel(parent)
    win.title("🔧 Update System Details")
    win.geometry("700x500")
    win.configure(bg="#E8F0FE")
    win.transient(parent)
    win.grab_set()

    tk.Label(win, text="Update System Details", font=("Helvetica", 18, "bold"), bg="#E8F0FE", fg="#1a73e8").pack(pady=20)

    frame = tk.Frame(win, bg="#ffffff", padx=30, pady=20)
    frame.pack(fill="both", expand=True, padx=40, pady=20)

    search_frame = tk.Frame(frame, bg="#ffffff")
    search_frame.pack(fill="x", pady=(0, 20))

    id_entry = ModernEntry(search_frame, "🆔 Enter System ID")
    id_entry.pack(side="left", expand=True, padx=(0, 10))

    status_label = tk.Label(frame, text="", font=("Helvetica", 10), bg="#ffffff", fg="#f44336")
    status_label.pack(pady=(5, 10))

    fields = {}

    fields['department'] = ModernEntry(frame, "🏫 Department")
    fields['department'].pack(fill="x", pady=10)

    fields['password'] = ModernEntry(frame, "🔒 Password", show="*")
    fields['password'].pack(fill="x", pady=10)



    original_data = {}

    def search_system():
        sid = id_entry.get_value().strip()
        if not sid:
            status_label.config(text="Please enter system ID", fg="#f44336")
            return
        try:
            url = f"http://localhost:8080/api/system/{id}"
            headers = {'Authorization': f'Bearer {token}'}
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                data = res.json()
                original_data.clear()
                original_data.update(data)
                fields['department'].set_value(data.get('department', ''))
                fields['password'].set_value(data.get('password', ''))
                fields['role'].set(data.get('role', 'FACULTY'))
                status_label.config(text="✅ System found", fg="#4CAF50")
            elif res.status_code == 404:
                status_label.config(text="❌ System not found", fg="#f44336")
            else:
                status_label.config(text=f"⚠️ Error: {res.status_code}", fg="#f44336")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}", fg="#f44336")

    def update_system():
        sid = id_entry.get_value().strip()
        if not sid:
            status_label.config(text="Please enter system ID", fg="#f44336")
            return

        dept = fields['department'].get_value().strip()
        pwd = fields['password'].get_value()
        

        if not dept or not pwd:
            status_label.config(text="All fields are required", fg="#f44336")
            return

        try:
            payload = {
                "system_id": int(sid),
                "department": dept,
                "password": pwd,
                
            }
        except ValueError:
            status_label.config(text="System ID must be a number", fg="#f44336")
            return

        try:
            res = requests.put(
                f"http://localhost:8080/api/system/update/{id}",
                data=json.dumps(payload),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                }
            )
            if res.status_code == 200:
                messagebox.showinfo("✅ Success", "System updated successfully")
                win.destroy()
            else:
                status_label.config(text=f"❌ Update failed: {res.status_code}", fg="#f44336")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}", fg="#f44336")

    tk.Button(search_frame, text="🔍 Search", command=search_system,
              bg="#1a73e8", fg="white", font=("Helvetica", 11, "bold"), relief="flat",
              padx=20, pady=6, cursor="hand2", activebackground="#155ab6").pack(side="right", pady=10)

    button_frame = tk.Frame(frame, bg="#ffffff")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="✅ Update", command=update_system,
              bg="#34A853", fg="white", font=("Helvetica", 12, "bold"), relief="flat",
              padx=25, pady=8, cursor="hand2", activebackground="#2c8b45").pack(side="left", padx=10)

    tk.Button(button_frame, text="❌ Cancel", command=win.destroy,
              bg="#EA4335", fg="white", font=("Helvetica", 12, "bold"), relief="flat",
              padx=25, pady=8, cursor="hand2", activebackground="#c72c1d").pack(side="left", padx=10)
