import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import re  # For email validation
from datetime import datetime
import requests  # Add this import for HTTP requests
import shutil
import json
from PIL import Image, ImageTk # Import Pillow for image handling
from face_encode import encodings
from Face import Face

class ModernEntry(tk.Frame):
    def __init__(self, parent, placeholder="", show=None, width_chars=None):
        super().__init__(parent, bg="#ffffff")

        self.placeholder = placeholder  # Store placeholder text
        self.entry = tk.Entry(self,
                               font=("Helvetica", 11),
                               bg="#ffffff",
                               fg="#333333",
                               bd=1,
                               relief=tk.SOLID,
                               show=show,
                               width=width_chars) # Set width for consistent sizing
        self.entry.pack(fill=tk.X, ipady=8, expand=True) # Allow horizontal expansion

        # Configure border color
        self.entry.configure(highlightthickness=1,
                               highlightbackground="#e0e0e0",
                               highlightcolor="#4CAF50")

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
        """Get the actual value, returning empty string if it's just placeholder"""
        value = self.entry.get()
        if value == self.placeholder:
            return ""
        return value

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_user_id(user_id):
    """Validate user ID format"""
    if not user_id:
        return False, "User ID is required!"
    if not user_id.isdigit():
        return False, "User ID must contain only numbers!"
    if len(user_id) != 11:
        return False, "User ID must be 11 digits!"
    return True, ""

def validate_name(name):
    """Validate full name"""
    if not name:
        return False, "Full name is required!"
    if len(name) < 3:
        return False, "Name must be at least 3 characters long!"
    if not all(x.isalpha() or x.isspace() for x in name):
        return False, "Name can only contain letters and spaces!"
    return True, ""

def validate_department(dept):
    """Validate department selection"""
    if dept == "Select Department":
        return False, "Please select a department!"
    return True, ""

def validate_year(year):
    """Validate year of passing"""
    if year == "Select Year":
        return False, "Please select year of passing!"
    return True, ""

def validate_password(password, confirm_password):
    """Validate password"""
    if not password:
        return False, "Password is required!"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long!"
    if password != confirm_password:
        return False, "Passwords do not match!"
    return True, ""

def validate_photo(photo_path):
    """Validate photo selection"""
    if not photo_path:
        return False, "Please select a photo!"
    return True, ""


def validate_all_inputs(user_data, photo_path, confirm_pwd):
    """Validate all inputs before submission"""
    # Validate User ID
    valid, message = validate_user_id(user_data['userid'])
    if not valid:
        return False, message

    # Validate Name
    valid, message = validate_name(user_data['name'])
    if not valid:
        return False, message

    # Validate Department
    valid, message = validate_department(user_data['department'])
    if not valid:
        return False, message

    # Validate Year
    valid, message = validate_year(str(user_data['yop']))
    if not valid:
        return False, message

    # Validate Email
    if not validate_email(user_data['email']):
        return False, "Please enter a valid email address!"

    # Validate Password
    valid, message = validate_password(user_data['password'], confirm_pwd)
    if not valid:
        return False, message

    # Validate Photo
    valid, message = validate_photo(photo_path)
    if not valid:
        return False, message

    return True, ""

class RegisterWindow:
    def __init__(self, parent, token):
        self.register_window = tk.Toplevel(parent)
        self.register_window.title("Create New Account")
        self.register_window.geometry("1000x700")
        self.register_window.configure(bg="#ffffff")

        # Initialize image references
        self.current_image = None
        self.preview_label = None

        # Enable minimize and maximize buttons
        self.register_window.resizable(True, True)
        self.register_window.minsize(1000, 700)

        # Make the window modal
        self.register_window.transient(parent)
        self.register_window.grab_set()

        # Main container with two columns
        self.main_container = tk.Frame(self.register_window, bg="#ffffff")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Left column - Form
        self.form_column = tk.Frame(self.main_container, bg="#ffffff")
        self.form_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Welcome text
        tk.Label(self.form_column,
                 text="Welcome",
                 font=("Helvetica", 32, "bold"),
                 fg="#4CAF50",
                 bg="#ffffff").pack(anchor=tk.W)

        tk.Label(self.form_column,
                 text="Register new account",
                 font=("Helvetica", 14),
                 fg="#666666",
                 bg="#ffffff").pack(anchor=tk.W, pady=(0, 30))

        # Form frame
        self.form_frame = tk.Frame(self.form_column, bg="#ffffff")
        self.form_frame.pack(fill=tk.X, pady=10, expand=True) # Allow form frame to expand horizontally

        # User ID and Name row
        self.id_name_frame = tk.Frame(self.form_frame, bg="#ffffff")
        self.id_name_frame.pack(fill=tk.X, pady=(0, 15))
        self.id_name_frame.grid_columnconfigure(0, weight=1) # Allow columns to expand
        self.id_name_frame.grid_columnconfigure(1, weight=1)

        # User ID
        self.userid_frame = tk.Frame(self.id_name_frame, bg="#ffffff")
        self.userid_frame.grid(row=0, column=0, sticky="ew", padx=(0, 15)) # Use grid for better control
        tk.Label(self.userid_frame,
                 text="User ID",
                 font=("Helvetica", 10),
                 fg="#666666",
                 bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        self.userid = ModernEntry(self.userid_frame, "", width_chars=30) # Set a base width
        self.userid.pack(fill=tk.X)

        # Name
        self.name_frame = tk.Frame(self.id_name_frame, bg="#ffffff")
        self.name_frame.grid(row=0, column=1, sticky="ew")
        tk.Label(self.name_frame,
                 text="Full Name",
                 font=("Helvetica", 10),
                 fg="#666666",
                 bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        self.name = ModernEntry(self.name_frame, "", width_chars=30) # Set a base width
        self.name.pack(fill=tk.X)

        # Department and YOP row
        self.dept_yop_frame = tk.Frame(self.form_frame, bg="#ffffff")
        self.dept_yop_frame.pack(fill=tk.X, pady=(0, 15))
        self.dept_yop_frame.grid_columnconfigure(0, weight=1) # Allow columns to expand
        self.dept_yop_frame.grid_columnconfigure(1, weight=1)

        # Department
        self.dept_frame = tk.Frame(self.dept_yop_frame, bg="#ffffff")
        self.dept_frame.grid(row=0, column=0, sticky="ew", padx=(0, 15))
        tk.Label(self.dept_frame,
                 text="Department",
                 font=("Helvetica", 10),
                 fg="#666666",
                 bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))

        departments = ["CSE", "ECE", "EE", "ME", "CE"]
        self.department_var = tk.StringVar(value='Select Department')
        self.department_menu = ttk.Combobox(self.dept_frame,
                                            textvariable=self.department_var,
                                            values=departments,
                                            width=27, # Adjusted width to match entry fields roughly
                                            state='readonly')
        self.department_menu.pack(fill=tk.X)

        # Year of Passing
        self.yop_frame = tk.Frame(self.dept_yop_frame, bg="#ffffff")
        self.yop_frame.grid(row=0, column=1, sticky="ew")
        tk.Label(self.yop_frame,
                 text="Year of Passing",
                 font=("Helvetica", 10),
                 fg="#666666",
                 bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))

        current_year = datetime.now().year
        self.years = list(range(current_year, current_year + 6))
        self.yop_var = tk.StringVar(value='Select Year')
        self.yop_menu = ttk.Combobox(self.yop_frame,
                                     textvariable=self.yop_var,
                                     values=self.years,
                                     width=27, # Adjusted width to match entry fields roughly
                                     state='readonly')
        self.yop_menu.pack(fill=tk.X)

        # Email
        self.email_frame = tk.Frame(self.form_frame, bg="#ffffff")
        self.email_frame.pack(fill=tk.X, pady=(0, 15))
        tk.Label(self.email_frame,
                 text="Email Account",
                 font=("Helvetica", 10),
                 fg="#666666",
                 bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        self.email = ModernEntry(self.email_frame, "Enter your email", width_chars=60) # Increased width for email
        self.email.pack(fill=tk.X) # Allow email entry to expand

        # Password fields row
        self.passwords_frame = tk.Frame(self.form_frame, bg="#ffffff")
        self.passwords_frame.pack(fill=tk.X, pady=(0, 25))
        self.passwords_frame.grid_columnconfigure(0, weight=1)
        self.passwords_frame.grid_columnconfigure(1, weight=1)

        # Password
        self.password_frame = tk.Frame(self.passwords_frame, bg="#ffffff")
        self.password_frame.grid(row=0, column=0, sticky="ew", padx=(0, 15))
        tk.Label(self.password_frame,
                 text="Password",
                 font=("Helvetica", 10),
                 fg="#666666",
                 bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        self.password = ModernEntry(self.password_frame, "", show="●", width_chars=30)
        self.password.pack(fill=tk.X)

        # Confirm Password
        self.confirm_frame = tk.Frame(self.passwords_frame, bg="#ffffff")
        self.confirm_frame.grid(row=0, column=1, sticky="ew")
        tk.Label(self.confirm_frame,
                 text="Confirm Password",
                 font=("Helvetica", 10),
                 fg="#666666",
                 bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        self.confirm_password = ModernEntry(self.confirm_frame, "", show="●", width_chars=30)
        self.confirm_password.pack(fill=tk.X)

        # Photo upload section
        self.photo_frame = tk.Frame(self.form_frame, bg="#ffffff")
        self.photo_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(self.photo_frame,
                 text="Profile Photo",
                 font=("Helvetica", 10),
                 fg="#666666",
                 bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))

        self.photo_label = tk.Label(self.photo_frame,
                                     text="No photo selected",
                                     font=("Helvetica", 10),
                                     fg="#666666",
                                     bg="#ffffff")
        self.photo_label.pack(side=tk.LEFT, padx=(10, 10))

        self.photo_path = [None]  # Using list to store path as a mutable object

        # Right column - Illustration/Photo Preview
        self.illustration_column = tk.Frame(self.main_container, bg="#ffffff", width=400)
        self.illustration_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(40, 0))

        # Create a frame for the preview with a border
        self.preview_border = tk.Frame(self.illustration_column, bg="#e0e0e0", padx=2, pady=2)
        self.preview_border.pack(expand=True, pady=20)

        # Create the preview label
        self.preview_label = tk.Label(self.preview_border, bg="#ffffff")
        self.preview_label.pack(expand=True)

        # Load and display the default illustration image
        try:
            self.display_image("photos/2.png") # Use the new helper function for initial display
        except Exception as e:
            print(f"Error loading illustration: {e}")
            pass

        def choose_photo():
            self.photo_path[0] = self.handle_photo_upload(self.photo_label)

        self.photo_btn = tk.Button(self.photo_frame,
                                   text="Choose Photo",
                                   font=("Helvetica", 10),
                                   bg="#4CAF50",
                                   fg="white",
                                   bd=0,
                                   padx=15,
                                   pady=5,
                                   cursor="hand2",
                                   command=choose_photo)
        self.photo_btn.pack(side=tk.LEFT)

        # Error label for displaying validation messages
        self.error_label = tk.Label(self.form_frame,
                                     text="",
                                     font=("Helvetica", 10),
                                     fg="#FF4444",
                                     bg="#ffffff")
        self.error_label.pack(pady=(0, 10))

        def send_user_data_to_server(user_data):
            try:
                server_data = {
                    'student_id': int(user_data['userid']),
                    'name': user_data['name'],
                    'yop': int(user_data['yop']),
                    'department': user_data['department'],
                    'email': user_data['email'],
                    'password': user_data['password'],
                    'role': 'STUDENT'
                }

                response = requests.post(
                    "http://localhost:8080/api/student/admin/register",
                    data=json.dumps(server_data),
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {token}'
                    }
                )

                if response.status_code == 200:
                    return True, "Data successfully sent to server"
                else:
                    return False, f"Server error: {response.status_code} - {response.text}"

            except requests.exceptions.ConnectionError:
                return False, "Connection failed: Please check if the server is running at localhost:8080"
            except requests.exceptions.Timeout:
                return False, "Request timed out: Server took too long to respond"
            except requests.exceptions.RequestException as e:
                return False, f"Network error: {str(e)}"
            except Exception as e:
                return False, f"Error sending data to server: {str(e)}"

        def submit_to_server():
            try:
                # Get values with error checking
                user_data = {
                    'userid': self.userid.get_value().strip(),
                    'name': self.name.get_value().strip(),
                    'department': self.department_var.get(),
                    'yop': self.yop_var.get(),
                    'email': self.email.get_value().strip(),
                    'password': self.password.get_value()
                }

                # Check for empty fields
                for key, value in user_data.items():
                    if not value or value in ['Select Department', 'Select Year']:
                        self.error_label.config(text=f"{key.capitalize()} is required!")
                        return

                # Validate all inputs
                valid, message = validate_all_inputs(user_data, self.photo_path[0], self.confirm_password.get_value())
                if not valid:
                    self.error_label.config(text=message)
                    return

                # Send data to server
                server_success, server_message = send_user_data_to_server(user_data)
                # Assuming 'encodings' is available from 'face_encode' and has face_encoding method
                # from face_encode import encodings # This import needs to be at the top level
                encodings.face_encoding(self.photo_path[0], user_data['name'], user_data['userid'])

                if server_success:
                    messagebox.showinfo("Success", "Account created successfully!")
                    self.register_window.destroy()
                else:
                    self.error_label.config(text=server_message)

            except Exception as e:
                error_msg = f"Error during submission: {str(e)}"
                print(error_msg)
                self.error_label.config(text=error_msg)

        # Submit button with modern style
        self.submit_btn = tk.Button(self.form_frame,
                                     text="Submit",
                                     font=("Helvetica", 12, "bold"),
                                     bg="#4CAF50",
                                     fg="white",
                                     padx=30,
                                     pady=12,
                                     bd=0,
                                     cursor="hand2",
                                     relief=tk.FLAT,
                                     command=submit_to_server)
        self.submit_btn.pack(pady=20)

        def on_submit_hover(e):
            self.submit_btn['bg'] = '#45a049'

        def on_submit_leave(e):
            self.submit_btn['bg'] = '#4CAF50'

        self.submit_btn.bind('<Enter>', on_submit_hover)
        self.submit_btn.bind('<Leave>', on_submit_leave)

        def on_closing():
            self.register_window.grab_release()
            self.register_window.destroy()

        self.register_window.protocol("WM_DELETE_WINDOW", on_closing)

    def display_image(self, image_path):
        """Helper function to load, resize, and display an image."""
        try:
            # Open image using Pillow
            pil_image = Image.open(image_path)

            # Get dimensions of the preview area
            # We assume a fixed size for the preview for consistency, adjust as needed
            frame_width = 400
            frame_height = 600

            # Calculate scaling to fit the frame while maintaining aspect ratio
            img_width, img_height = pil_image.size
            width_ratio = frame_width / img_width
            height_ratio = frame_height / img_height
            scale_factor = min(width_ratio, height_ratio)

            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)

            # Resize image
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.current_image = ImageTk.PhotoImage(pil_image)

            # Update the preview label
            self.preview_label.config(image=self.current_image)

        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}")
            self.preview_label.config(image='') # Clear the image if not found
            self.current_image = None
        except Exception as e:
            print(f"Error displaying image preview: {e}")
            self.preview_label.config(image='') # Clear the image on other errors
            self.current_image = None


    def handle_photo_upload(self, photo_label):
        """Handle photo upload functionality"""
        image_dir = "user_photos"
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        file_types = [('Image files', '*.png *.jpg *.jpeg *.gif *.bmp')]
        file_path = filedialog.askopenfilename(filetypes=file_types)

        if file_path:
            try:
                filename = os.path.basename(file_path)
                dest_path = os.path.join(image_dir, filename)
                shutil.copy2(file_path, dest_path)

                photo_label.config(text=filename)
                self.display_image(file_path) # Use the helper function to display the chosen image

                return filename
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save photo: {str(e)}")
                return None
        return None

def create_register_window(parent, token):
    return RegisterWindow(parent, token).register_window