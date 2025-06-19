import tkinter as tk
from PIL import Image, ImageTk

def create_button(parent, text, color_code, command=None):
    bg_color = color_code
    # Create slightly darker hover color
    r = int(color_code[1:3], 16)
    g = int(color_code[3:5], 16)
    b = int(color_code[5:7], 16)
    hover_color = f'#{max(0, r-30):02x}{max(0, g-30):02x}{max(0, b-30):02x}'
        
    btn = tk.Button(parent,
                   text=text,
                   font=("Helvetica", 12, "bold"),
                   bg=bg_color,
                   fg="white",
                   bd=1,
                   width=18,
                   pady=12,
                   padx=20,
                   cursor="hand2",
                   relief="flat",
                   command=command)
    
    def on_enter(e):
        btn['bg'] = hover_color
            
    def on_leave(e):
        btn['bg'] = bg_color
        
    btn.bind('<Enter>', on_enter)
    btn.bind('<Leave>', on_leave)
    return btn

def create_facylty_panel(token, admin_id):
    root = tk.Tk()
    root.title("Admin Panel")
    root.geometry("1400x800")
    root.configure(bg="#E6F9F9")  # Light turquoise background
    root.resizable(True, True)
    root.minsize(1300, 800)  # Set minimum window size

    # --- Button Functions ---
    def manual_attendence():
        from manual_attendance import create_manual_attendance_window
        create_manual_attendance_window(root, token, admin_id)

    def attendence_record():
        from attendance_record import create_attendance_window
        create_attendance_window(root, token)

    def logout():
        root.destroy()
        from main import main
        main()

    # --- Main Layout ---
    main_frame = tk.Frame(root, bg="white")
    main_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)

    left_frame = tk.Frame(content_frame, bg="white")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    title = tk.Label(left_frame, 
                    text="Admin Panel", 
                    font=("Helvetica", 48, "bold"),
                    bg="white",
                    fg="#002B5B",
                    justify=tk.LEFT)
    title.pack(anchor=tk.W)

    description = tk.Label(left_frame,
                         text="Manage users and attendance records\nwith advanced admin controls",
                         font=("Helvetica", 18),
                         bg="white",
                         fg="#666666",
                         justify=tk.LEFT)
    description.pack(anchor=tk.W, pady=(20, 40))

    buttons_frame = tk.Frame(left_frame, bg="white")
    buttons_frame.pack(anchor=tk.W)

    # Row 1
    row1_frame = tk.Frame(buttons_frame, bg="white")
    row1_frame.pack(anchor=tk.W, pady=(0, 15))

    manual_attendence_btn = create_button(row1_frame, "Manual Attendance", "#FF6B6B", manual_attendence)
    manual_attendence_btn.pack(side=tk.LEFT, padx=(0, 15))

    # Row 2
    row2_frame = tk.Frame(buttons_frame, bg="white")
    row2_frame.pack(anchor=tk.W, pady=(0, 15))

    attendence_record_btn = create_button(row2_frame, "Attendance Record", "#45B7D1", attendence_record)
    attendence_record_btn.pack(side=tk.LEFT, padx=(0, 15))

    # Row 3 - Logout button
    row3_frame = tk.Frame(buttons_frame, bg="white")
    row3_frame.pack(anchor=tk.W)

    logout_btn = create_button(row3_frame, "Logout", "#FF4C4C", logout)
    logout_btn.pack(side=tk.LEFT, padx=(0, 15))

    # Right Image
    try:
        img = Image.open("photos/adminimage.png")
        img = img.resize((600, 600), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(content_frame, image=photo, bg="white")
        img_label.image = photo
        img_label.pack(side=tk.RIGHT, padx=(50, 0))
    except:
        wave_frame = tk.Frame(content_frame, bg="#00B4B4", width=500, height=500)
        wave_frame.pack(side=tk.RIGHT, padx=(50, 0))
        wave_frame.pack_propagate(False)

    def on_closing():
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
