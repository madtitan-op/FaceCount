import tkinter as tk
from tkinter import ttk, messagebox
import requests

class ModernEntry(tk.Frame):
    def __init__(self, parent, label_text, show=None):
        super().__init__(parent, bg="#F5E6E0")
        self.label = tk.Label(self, text=label_text, font=("Helvetica", 10, "bold"), bg="#F5E6E0", fg="#333333")
        self.label.pack(anchor="w")

        self.entry = tk.Entry(self, font=("Helvetica", 12), bg="#ffffff", fg="#333333", relief="flat", bd=2,
                              highlightthickness=1, highlightbackground="#cccccc", highlightcolor="#4CAF50", show=show)
        self.entry.pack(fill="x", pady=(5, 0), ipady=4)

    def get_value(self):
        return self.entry.get()

def create_delete_window(parent, token):
    delete_window = tk.Toplevel(parent)
    delete_window.title("Delete User")
    delete_window.geometry("600x450")
    delete_window.configure(bg="#F5E6E0")

    if parent:
        delete_window.transient(parent)
        delete_window.grab_set()

    # Main container
    main_frame = tk.Frame(delete_window, bg="#F5E6E0", padx=40, pady=30)
    main_frame.pack(fill="both", expand=True)

    # Title
    title_label = tk.Label(main_frame, text="🔴 Delete User", font=("Helvetica", 22, "bold"),
                           bg="#F5E6E0", fg="#333333")
    title_label.pack(pady=(0, 30))

    # Search section
    search_frame = tk.Frame(main_frame, bg="#F5E6E0")
    search_frame.pack(fill="x", pady=(0, 20))

    roll_entry = ModernEntry(search_frame, "🎓 Roll Number")
    roll_entry.pack(side="left", expand=True, padx=(0, 10))

    search_button = tk.Button(search_frame, text="Search 🔍", command=lambda: search_user(),
                              bg="#4CAF50", fg="white", font=("Helvetica", 11, "bold"),
                              relief="flat", padx=16, pady=6, cursor="hand2")
    search_button.pack(side="left")

    # Details display area
    details_frame = tk.Frame(main_frame, bg="#F5E6E0")
    details_frame.pack(fill="x", pady=20)

    status_label = tk.Label(main_frame, text="", font=("Helvetica", 10), bg="#F5E6E0", fg="#666666")
    status_label.pack(pady=10)

    def search_user():
        rollno = roll_entry.get_value().strip()
        if not rollno:
            status_label.config(text="⚠️ Please enter a roll number", fg="#f44336")
            return

        try:
            response = requests.get(
                f"http://localhost:8080/api/student/admin/details/{rollno}",
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                }
            )

            for widget in details_frame.winfo_children():
                widget.destroy()

            if response.status_code == 401:
                status_label.config(text="❌ Authentication failed. Please login again.", fg="#f44336")
            elif response.status_code == 200:
                user = response.json()
                details_text = (
                    f"👤 Name: {user.get('name', 'N/A')}\n"
                    f"📧 Email: {user.get('email', 'N/A')}\n"
                    f"🏢 Department: {user.get('department', 'N/A')}\n"
                    f"🎓 Year of Passing: {user.get('yop', 'N/A')}"
                )
                tk.Label(details_frame, text=details_text, font=("Helvetica", 12),
                         bg="#F5E6E0", fg="#333333", justify="left").pack(anchor="w")
                status_label.config(text="✅ User found successfully", fg="#4CAF50")
            elif response.status_code == 404:
                status_label.config(text="❌ User not found", fg="#f44336")
            else:
                status_label.config(text=f"❌ Error: {response.status_code} - {response.text}", fg="#f44336")

        except requests.exceptions.ConnectionError:
            status_label.config(text="🌐 Cannot connect to server. Is it running?", fg="#f44336")
        except Exception as e:
            status_label.config(text=f"❌ Error: {str(e)}", fg="#f44336")

    def delete_user():
        student_id = roll_entry.get_value().strip()
        if not student_id:
            status_label.config(text="⚠️ Please enter a roll number", fg="#f44336")
            return

        confirm = messagebox.askyesno("Confirm Deletion",
                                      "Are you sure you want to delete this user?\nThis action cannot be undone.")
        if not confirm:
            return

        try:
            response = requests.delete(
                f"http://localhost:8080/api/student/admin/delete/{student_id}",
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}'
                }
            )

            if response.status_code == 200:
                messagebox.showinfo("Success", "✅ User deleted successfully")
                delete_window.destroy()
            elif response.status_code == 404:
                status_label.config(text="❌ User not found", fg="#f44336")
            elif response.status_code == 401:
                status_label.config(text="❌ Authentication failed. Please login again.", fg="#f44336")
            else:
                status_label.config(text=f"❌ Error: {response.status_code}", fg="#f44336")

        except requests.exceptions.ConnectionError:
            status_label.config(text="🌐 Cannot connect to server. Is it running?", fg="#f44336")
        except Exception as e:
            status_label.config(text=f"❌ Error: {str(e)}", fg="#f44336")

    # Buttons
    button_frame = tk.Frame(main_frame, bg="#F5E6E0")
    button_frame.pack(pady=20)

    delete_button = tk.Button(button_frame, text="🗑️ Delete", command=delete_user,
                              bg="#f44336", fg="white", font=("Helvetica", 12, "bold"),
                              relief="flat", padx=24, pady=6, cursor="hand2")
    delete_button.pack(side="left", padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel ❌", command=delete_window.destroy,
                              bg="#888888", fg="white", font=("Helvetica", 12, "bold"),
                              relief="flat", padx=24, pady=6, cursor="hand2")
    cancel_button.pack(side="left", padx=10)

    return delete_window
