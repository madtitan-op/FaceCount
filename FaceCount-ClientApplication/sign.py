import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
# Assuming get_token is defined in login.py
from login import get_token

class ModernEntry(tk.Frame):
    """A custom Entry widget with placeholder text and modern styling."""
    def __init__(self, parent, placeholder="", show=None, width=30):
        super().__init__(parent, bg="#F7F9FC") # Slightly off-white background

        self.placeholder = placeholder
        self.entry_var = tk.StringVar() # Use StringVar for better control
        
        self.entry = tk.Entry(self,
                              textvariable=self.entry_var,
                              font=("Segoe UI", 11), # Modern font
                              bg="#F7F9FC", # Background for the entry itself
                              fg="#333333",
                              bd=1,
                              relief=tk.SOLID,
                              show=show,
                              width=width)
        
        self.entry.pack(fill=tk.X, ipady=8, padx=1) # ipady for internal padding, padx for small border effect
        
        # Configure border color
        self.entry.configure(highlightthickness=1,
                             highlightbackground="#D9DCE0", # Light gray border
                             highlightcolor="#2196F3") # Blue focus color

        if placeholder:
            self.entry.insert(0, placeholder)
            self.entry.config(fg="#999999") # Placeholder text color
            
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        
        # Store original border color for hover effect
        self._original_highlightbackground = "#D9DCE0"
        self._hover_highlightbackground = "#A3A7AF" # Darker gray on hover

        self.entry.bind("<Enter>", self._on_enter)
        self.entry.bind("<Leave>", self._on_leave)

    def _on_focus_in(self, e):
        if self.entry_var.get() == self.placeholder:
            self.entry_var.set("")
            self.entry.config(fg="#333333")
            
    def _on_focus_out(self, e):
        if not self.entry_var.get():
            self.entry_var.set(self.placeholder)
            self.entry.config(fg="#999999")

    def _on_enter(self, e):
        # Change border color on hover only if not focused
        if str(self.entry) != self.master.focus_get(): # Check if it's not the currently focused widget
            self.entry.config(highlightbackground=self._hover_highlightbackground)

    def _on_leave(self, e):
        # Restore original border color when not hovering and not focused
        if str(self.entry) != self.master.focus_get():
            self.entry.config(highlightbackground=self._original_highlightbackground)

    def get_value(self):
        """Get the actual value, returning empty string if it's just placeholder"""
        value = self.entry_var.get()
        if value == self.placeholder:
            return ""
        return value

    def set_value(self, value):
        """Set the value of the entry widget, clearing placeholder if present."""
        self.entry_var.set(value)
        self.entry.config(fg="#333333") # Ensure text color is set to active
        if value:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, value)
            self.entry.config(fg="#333333") # Ensure text color is set to active
        else:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg="#999999")


class SignInWindow:
    def __init__(self):
        self.root = tk.Tk()
            
        self.root.title("Sign In") # Capitalized for consistency
        self.root.geometry("900x600") # Fixed size for simpler design
        self.root.resizable(False, False) # Keep non-resizable for fixed layout
        self.root.configure(bg="#E6EAF0") # Lighter background for the entire window

        # Center window (already good, just moved for structure)
        self._center_window(900, 600)

        # --- Styling Configuration ---
        self._setup_styles()

        # Main container using grid for better control
        main_frame = tk.Frame(self.root, bg="#E6EAF0")
        main_frame.pack(expand=True, fill="both", padx=30, pady=30) # Adjusted padding

        main_frame.grid_columnconfigure(0, weight=1) # Left side for illustration
        main_frame.grid_columnconfigure(1, weight=1) # Right side for form
        main_frame.grid_rowconfigure(0, weight=1)

        # Left side with illustration
        left_frame = tk.Frame(main_frame, bg="#E6EAF0")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20)) # Added padx
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        # Load illustration
        self.photo = None # Initialize photo reference
        try:
            image_path = os.path.join(os.path.dirname(__file__), "photos/login.png")
            img = Image.open(image_path)
            
            # Resize image to fit, maintaining aspect ratio
            # Max dimensions for image within its frame
            max_img_width = 350
            max_img_height = 350
            img.thumbnail((max_img_width, max_img_height), Image.LANCZOS)
            
            self.photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(left_frame, image=self.photo, bg="#E6EAF0")
            img_label.grid(row=0, column=0, pady=50, sticky="") # Centered within grid cell
        except Exception as e:
            print(f"Image load error: {e}")
            tk.Label(left_frame, text="Illustration", font=("Segoe UI", 24), bg="#E6EAF0", fg="#666666").grid(row=0, column=0, pady=50)

        # Right side with form - now uses a slightly different background for the form area
        right_frame = tk.Frame(main_frame, bg="#ffffff", bd=2, relief="flat", highlightbackground="#D9DCE0", highlightthickness=1) # White background for form, subtle border
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(20, 0)) # Added padx
        
        # Inner frame for padding and alignment within the right_frame
        inner_right_frame = tk.Frame(right_frame, bg="#ffffff")
        inner_right_frame.pack(expand=True, fill="both", padx=40, pady=40) # Padding inside the white box

        # Sign in title
        tk.Label(inner_right_frame, text="Welcome Back!", font=("Segoe UI", 28, "bold"), bg="#ffffff", fg="#333333").pack(pady=(0, 10))
        tk.Label(inner_right_frame, text="Sign in to your account.", font=("Segoe UI", 12), bg="#ffffff", fg="#666666").pack(pady=(0, 40))

        # Username field
        tk.Label(inner_right_frame, text="Username", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#444444").pack(anchor="w", pady=(0, 5))
        self.username_entry = ModernEntry(inner_right_frame, placeholder="Enter your username", width=40)
        self.username_entry.pack(fill="x", pady=(0, 20))

        # Password field
        tk.Label(inner_right_frame, text="Password", font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#444444").pack(anchor="w", pady=(0, 5))
        self.password_entry = ModernEntry(inner_right_frame, placeholder="Enter your password", show="•", width=40)
        self.password_entry.pack(fill="x", pady=(0, 30))

        # Sign in button
        sign_in_btn = tk.Button(inner_right_frame, text="Sign In", command=self.sign_in,
                                font=("Segoe UI", 13, "bold"), bg="#2196F3", fg="white", # Primary blue
                                relief="flat", padx=30, pady=12, cursor="hand2", # Hand cursor
                                activebackground="#1976D2", activeforeground="white") # Darker blue on click
        sign_in_btn.pack(pady=10)
        
        # Bind Enter key to self.sign_in
        self.root.bind('<Return>', lambda event: self.sign_in())

        # Progress bar (moved to be above the button, or where visually appropriate)
        # It was placed before the button. If it's for showing loading, it might be better
        # to pack it dynamically or hide it until needed. For now, keeping its position.
        # It should be initialized after styles are configured.
        self.progress_bar = ttk.Progressbar(inner_right_frame, length=250, mode='indeterminate', style="Blue.Horizontal.TProgressbar")
        self.progress_bar.pack(pady=10)
        self.progress_bar.stop() # Start it only when an action begins (e.g., sign in attempt)

        # Error label (new element)
        self.error_label = tk.Label(inner_right_frame, text="", font=("Segoe UI", 10), bg="#ffffff", fg="#FF4444")
        self.error_label.pack(pady=(5, 0))

        # Optional: "Don't have an account?" link - if you want a registration flow
        # tk.Label(inner_right_frame, text="Don't have an account?", font=("Segoe UI", 10), bg="#ffffff", fg="#666666").pack(pady=(20, 0))
        # register_link = tk.Label(inner_right_frame, text="Register Here", font=("Segoe UI", 10, "underline"), bg="#ffffff", fg="#2196F3", cursor="hand2")
        # register_link.pack()
        # register_link.bind("<Button-1>", lambda e: print("Open Register Window")) # Replace with actual command

    def _center_window(self, width, height):
        """Centers the Tkinter window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _setup_styles(self):
        """Configures ttk styles for consistent modern look."""
        style = ttk.Style()
        style.theme_use('clam') # 'clam' is good for customization

        # Progress bar style
        style.configure("Blue.Horizontal.TProgressbar",
                        troughcolor="#E6EAF0", # Lighter background for the trough
                        background="#2196F3", # Primary blue for the bar
                        thickness=10,
                        bordercolor="#D9DCE0",
                        lightcolor="#D9DCE0",
                        darkcolor="#D9DCE0",
                        relief=tk.FLAT)
        # You can add more styles for other widgets if needed
        
    def sign_in(self):
        self.error_label.config(text="") # Clear previous errors
        self.progress_bar.start(10) # Start progress bar animation

        username = self.username_entry.get_value() # Use get_value from ModernEntry
        password = self.password_entry.get_value() # Use get_value from ModernEntry
        admin_id=username
        
        if not username or not password:
            self.progress_bar.stop() # Stop on error
            self.error_label.config(text="Please enter both username and password!")
            # messagebox.showwarning("Error", "Please enter both username and password") # Alternative
            return

        # Simulate network request or actual API call
        # It's better to run network requests in a separate thread to keep GUI responsive
        # For this example, keeping it direct for simplicity.
        token = get_token(username, password) # Assuming this function handles the actual API call

        self.progress_bar.stop() # Stop progress bar after request

        if token:
            messagebox.showinfo("Success", "Sign in successful!")
            self.root.destroy()
            from admin_panel import create_admin_panel
            create_admin_panel(token, admin_id) # Pass username as admin_id
        else:
            self.error_label.config(text="Authentication failed! Please check your credentials.")
            # messagebox.showerror("Error", "Authentication failed") # Alternative

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = SignInWindow()
    app.run()