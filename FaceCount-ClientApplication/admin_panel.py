import tkinter as tk
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox

def create_button(parent, text, color_code, command=None):
    bg_color = color_code
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

def create_admin_panel(token, admin_id):
    root = tk.Tk()
    root.title("Admin Panel")
    root.geometry("1400x800")
    root.configure(bg="#E6F9F9")
    root.resizable(True, True)
    root.minsize(1300, 800)

    # --- Admin Functionalities ---
    def register_user():
        from register_user import create_register_window
        create_register_window(root, token)

    def admin_register():
        from admin_register import create_admin_register_window
        create_admin_register_window(root, token)

    def modify_user():
        from modify_user import create_modify_window
        create_modify_window(root, token)

    def delete_user():
        from delete_user import create_delete_window
        create_delete_window(root, token)

    def system_register():
        from system_register import create_system_register_window
        create_system_register_window(root, token)

    def faculty_register():
        from admin_register import create_admin_register_window
        create_admin_register_window(root, token)

    def update_faculty():
        from update_faculty import create_faculty_modify_window
        create_faculty_modify_window(root, token)

    def delete_faculty():
        from delete_faculty import create_faculty_delete_window
        create_faculty_delete_window(root,token)

    def update_system():
        from update_system import create_system_update_window
        create_system_update_window(root,token)
    def delete_system():
        # TODO: Implement system deletion functionality
        messagebox.showinfo("Coming Soon", "System deletion functionality will be implemented soon!")

    def logout():
        root.destroy()
        from main import main
        main()

    # --- Main Panel UI ---
    main_frame = tk.Frame(root, bg="white")
    main_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

    content_frame = tk.Frame(main_frame, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=30)

    # Left Side Content
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

    # Create buttons with modern styling
    button_style = {
        'font': ('Segoe UI', 12, 'bold'),
        'bg': '#4CAF50',
        'fg': 'white',
        'padx': 20,
        'pady': 10,
        'bd': 0,
        'relief': 'flat',
        'cursor': 'hand2'
    }

    # First row - Register buttons
    register_user_btn = tk.Button(buttons_frame, text="Register Student", command=register_user, **button_style)
    register_user_btn.grid(row=0, column=0, padx=10, pady=10, sticky='ew')
    register_user_btn.bind('<Enter>', lambda e: register_user_btn.config(bg='#45a049'))
    register_user_btn.bind('<Leave>', lambda e: register_user_btn.config(bg='#4CAF50'))

    faculty_register_btn = tk.Button(buttons_frame, text="Register Faculty", command=faculty_register, **button_style)
    faculty_register_btn.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
    faculty_register_btn.bind('<Enter>', lambda e: faculty_register_btn.config(bg='#45a049'))
    faculty_register_btn.bind('<Leave>', lambda e: faculty_register_btn.config(bg='#4CAF50'))

    system_register_btn = tk.Button(buttons_frame, text="Register System", command=system_register, **button_style)
    system_register_btn.grid(row=0, column=2, padx=10, pady=10, sticky='ew')
    system_register_btn.bind('<Enter>', lambda e: system_register_btn.config(bg='#45a049'))
    system_register_btn.bind('<Leave>', lambda e: system_register_btn.config(bg='#4CAF50'))

    # Second row - Update buttons
    update_user_btn = tk.Button(buttons_frame, text="Update Student", command=modify_user, **button_style)
    update_user_btn.grid(row=1, column=0, padx=10, pady=10, sticky='ew')
    update_user_btn.bind('<Enter>', lambda e: update_user_btn.config(bg="#14b5d1"))
    update_user_btn.bind('<Leave>', lambda e: update_user_btn.config(bg="#4C7DAA"))

    update_faculty_btn = tk.Button(buttons_frame, text="Update Faculty", command=update_faculty, **button_style)
    update_faculty_btn.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
    update_faculty_btn.bind('<Enter>', lambda e: update_faculty_btn.config(bg="#4583a0"))
    update_faculty_btn.bind('<Leave>', lambda e: update_faculty_btn.config(bg="#2B6C77"))

    update_system_btn = tk.Button(buttons_frame, text="Update System", command=update_system, **button_style)
    update_system_btn.grid(row=1, column=2, padx=10, pady=10, sticky='ew')
    update_system_btn.bind('<Enter>', lambda e: update_system_btn.config(bg="#458ea0"))
    update_system_btn.bind('<Leave>', lambda e: update_system_btn.config(bg="#1CC7C7"))

    # Third row - Delete buttons
    delete_user_btn = tk.Button(buttons_frame, text="Delete Student", command=delete_user, **button_style)
    delete_user_btn.grid(row=2, column=0, padx=10, pady=10, sticky='ew')
    delete_user_btn.bind('<Enter>', lambda e: delete_user_btn.config(bg="#d12424"))
    delete_user_btn.bind('<Leave>', lambda e: delete_user_btn.config(bg="#B96934"))

    delete_faculty_btn = tk.Button(buttons_frame, text="Delete Faculty", command=delete_faculty, **button_style)
    delete_faculty_btn.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
    delete_faculty_btn.bind('<Enter>', lambda e: delete_faculty_btn.config(bg="#db0b1d"))
    delete_faculty_btn.bind('<Leave>', lambda e: delete_faculty_btn.config(bg="#913524"))

    delete_system_btn = tk.Button(buttons_frame, text="Delete System", command=delete_system, **button_style)
    delete_system_btn.grid(row=2, column=2, padx=10, pady=10, sticky='ew')
    delete_system_btn.bind('<Enter>', lambda e: delete_system_btn.config(bg="#e61010"))
    delete_system_btn.bind('<Leave>', lambda e: delete_system_btn.config(bg="#A35F32"))

     # Fourth row - Logout button
    logout_btn = tk.Button(buttons_frame, text="Logout", command=logout, **button_style)
    logout_btn.grid(row=3, column=1, padx=10, pady=30, sticky='ew')
    logout_btn.bind('<Enter>', lambda e: logout_btn.config(bg="#f44336"))
    logout_btn.bind('<Leave>', lambda e: logout_btn.config(bg="#4CAF50"))

    # Configure grid weights
    buttons_frame.grid_columnconfigure(0, weight=1)
    buttons_frame.grid_columnconfigure(1, weight=1)
    buttons_frame.grid_columnconfigure(2, weight=1)

    # Right Side Image
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

    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
