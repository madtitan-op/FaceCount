import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

def create_hover_effect(button):
    def on_enter(e):
        button['fg'] = '#E88D72'
    def on_leave(e):
        button['fg'] = '#2B2B2B'
    button.bind('<Enter>', on_enter)
    button.bind('<Leave>', on_leave)

def create_button(parent, text, bg_color, command=None):
    btn = tk.Button(parent,
                   text=text,
                   font=("Arial", 16, "bold"),
                   bg=bg_color,
                   fg="white",
                   bd=0,
                   width=20,
                   pady=15,
                   cursor="hand2",
                   command=command)
    
    def on_enter(e):
        if bg_color == "#E88D72":
            btn['bg'] = '#D67D62'
        elif bg_color == "#2B2B2B":
            btn['bg'] = '#404040'
        else:
            btn['bg'] = '#808080'
            
    def on_leave(e):
        btn['bg'] = bg_color
        
    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)
    return btn

def main():
    root = tk.Tk()
    root.title("FaceCount - Attendance System")
    root.geometry("1300x800")
    root.configure(bg="#F5E6E0")
    
    main_frame = tk.Frame(root, bg="#F5E6E0")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)
    
    left_frame = tk.Frame(main_frame, bg="#F5E6E0")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    title_frame = tk.Frame(left_frame, bg="#F5E6E0")
    title_frame.pack(anchor=tk.W)
    
    title = tk.Label(title_frame, 
                    text="FACECOUNT", 
                    font=("Arial Black", 48, "bold"),
                    bg="#F5E6E0",
                    fg="#2B2B2B",
                    justify=tk.LEFT,
                    )
    title.pack(anchor=tk.W)
    
    subtitle_frame = tk.Frame(left_frame, bg="#F5E6E0")
    subtitle_frame.pack(anchor=tk.W, pady=(20, 40))
    
    subtitle = tk.Label(subtitle_frame,
                       text="A FACE RECOGNITION\nBASED ATTENDANCE SYSTEM",
                       font=("Arial", 36),
                       bg="#F5E6E0",
                       fg="#666666",
                       justify=tk.LEFT)
    subtitle.pack(anchor=tk.W)
    
    description = tk.Label(left_frame,
                          text="To Mark Attendance\nScan Your Face",
                          font=("Arial", 14),
                          bg="#F5E6E0",
                          fg="#2B2B2B",
                          justify=tk.LEFT)
    description.pack(anchor=tk.W)

    
    # Buttons Frame
    buttons_frame = tk.Frame(left_frame, bg="#F5E6E0")
    buttons_frame.pack(anchor=tk.W, pady=(40, 0))
    
    # Create all three buttons with equal styling
    def mark_attendance():
        root.destroy()
        from attendance_sign_in import AttendanceSignInWindow
        app = AttendanceSignInWindow()
        app.run()
    
    mark_attendance_btn = create_button(buttons_frame, "Mark Attendance", "#E88D72", mark_attendance)
    mark_attendance_btn.pack(anchor=tk.W, pady=(0, 20))
    
    def open_admin():
        root.destroy()
        from sign import SignInWindow
        app = SignInWindow()
        app.run()
    
    admin_btn = create_button(buttons_frame, "Admin", "#2B2B2B", open_admin)
    admin_btn.pack(anchor=tk.W, pady=(0, 20))
    
    def open_faculty_login():
        root.destroy() # Destroy main window before opening new login window
        from faculty_sign import FacultySignInWindow # Use faculty_sign.py
        app = FacultySignInWindow()
        app.run()
    
    faculty_btn = create_button(buttons_frame, "Faculty", "#666666", open_faculty_login)
    faculty_btn.pack(anchor=tk.W)
    
    # Right side date frame
    date_frame = tk.Frame(main_frame, bg="#F5E6E0")
    date_frame.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Current date display
    current_date = datetime.now().strftime("%B %d, %Y")
    date_label = tk.Label(date_frame,
                         text=current_date,
                         font=("Arial", 16, "bold"),
                         bg="#F5E6E0",
                         fg="#2B2B2B",
                         justify=tk.RIGHT)
    date_label.pack(anchor=tk.E, pady=10)

    # Try to load and display the illustration
    try:
        img = Image.open("photos/1.png")
        img = img.resize((500, 500), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(main_frame, image=photo, bg="#F5E6E0")
        img_label.image = photo
        img_label.place(relx=0.6, rely=0.4)
    except:
        placeholder = tk.Frame(main_frame, bg="#E88D72", width=400, height=300)
        placeholder.place(relx=0.5, rely=0.4)

    root.mainloop()

if __name__ == "__main__":
    main()
