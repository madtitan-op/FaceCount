import tkinter as tk
from tkinter import  messagebox
from login import get_token

class AttendanceSignInWindow:
    def __init__(self, parent=None):
        if parent:
            self.root = tk.Toplevel(parent)
            self.root.transient(parent)
            self.root.grab_set()
        else:
            self.root = tk.Tk()
        self.root.title("Sign In")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f7f6fd")

        # Main split frame
        split_frame = tk.Frame(self.root, bg="#f7f6fd")
        split_frame.pack(fill="both", expand=True)

        # Left: Login form
        left_frame = tk.Frame(split_frame, bg="#f7f6fd", width=500)
        left_frame.pack(side="left", fill="both", expand=True)
        left_frame.pack_propagate(False)

        # Top circle
        canvas = tk.Canvas(left_frame, width=60, height=60, bg="#f7f6fd", highlightthickness=0)
        canvas.pack(pady=(40, 10))
        canvas.create_oval(50, 50, 50, 50, outline="#a18cd1", width=4)

        # Title
        tk.Label(left_frame, text="Log in / For Scan Your Face", font=("Segoe UI", 16, "bold"), fg="#7b5ff5", bg="#f7f6fd").pack(pady=(0, 30))

        # User ID field
        tk.Label(left_frame, text="User ID", font=("Arial", 12), bg="#f7f6fd").pack(anchor="w", padx=60)
        self.userid_entry = tk.Entry(left_frame, font=("Arial", 12), bg="#F0F0F0", fg="#2B2B2B", relief="flat")
        self.userid_entry.pack(fill="x", padx=60, pady=(5, 18), ipady=7)

        # Password field
        tk.Label(left_frame, text="Password", font=("Arial", 12), bg="#f7f6fd").pack(anchor="w", padx=60)
        self.password_entry = tk.Entry(left_frame, font=("Arial", 12), bg="#F0F0F0", fg="#2B2B2B", relief="flat", show="•")
        self.password_entry.pack(fill="x", padx=60, pady=(5, 10), ipady=7)

        # Log in button (gradient effect simulated)
        def on_enter(e):
            login_btn.config(bg="#fbc2eb")
        def on_leave(e):
            login_btn.config(bg="#a18cd1")
        login_btn = tk.Button(left_frame, text="Log in", command=self.sign_in, font=("Segoe UI", 13, "bold"), bg="#a18cd1", fg="white", relief="flat", activebackground="#fbc2eb", activeforeground="#7b5ff5", cursor="hand2")
        login_btn.pack(fill="x", padx=60, pady=(10, 10), ipady=7)
        login_btn.bind('<Enter>', on_enter)
        login_btn.bind('<Leave>', on_leave)

       

       
        # Right: Circle info panel
        right_frame = tk.Canvas(split_frame, width=500, height=1000, bg="#f7f6fd", highlightthickness=0)
        right_frame.pack(side="right", fill="both", expand=True)
        # Draw diagonal lines ("/" style) with gradient colors
        line_colors = ["#a18cd1", "#fbc2eb", "#fbc2eb", "#a18cd1", "#a18cd1", "#fbc2eb", "#a18cd1", "#fbc2eb", "#a18cd1", "#fbc2eb"]
        for i, color in enumerate(line_colors):
            x_offset = 60 + i*40
            right_frame.create_line(x_offset, 0, 500 + x_offset, 600, fill=color, width=18)

        self.root.bind('<Return>', lambda event: self.sign_in())

    def sign_in(self):
        userid = self.userid_entry.get().strip()
        password = self.password_entry.get().strip()
        system_id = userid
        if not userid or not password:
          
            messagebox.showwarning("Error", "Please enter both user ID and password")
        else:
            token = get_token(userid, password)
            if token:
                
                #self.root.destroy()
                from f_main import cam_read
                cam_read(token,system_id)
               
            else:
                messagebox.showerror("Error", "Authentication failed")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AttendanceSignInWindow()
    app.run() 