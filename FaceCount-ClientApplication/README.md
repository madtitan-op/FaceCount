# FaceCount - Face Recognition Attendance System

## Overview
FaceCount is a face recognition-based attendance system with a graphical user interface (GUI) built using Python and Tkinter. It allows students, faculty, and administrators to mark and manage attendance efficiently and securely using facial recognition technology.

## Features
- **Face Recognition Attendance:** Mark attendance by scanning your face.
- **User Registration:** Register new students and faculty with photo and details.
- **Admin Panel:** Manage users, view attendance records, and perform manual attendance.
- **Faculty Panel:** Faculty can view and manage their attendance records.
- **Secure Data Handling:** Uses encryption for sensitive data.
- **Modern GUI:** User-friendly interface with modern design elements.

## Directory Structure
```
FaceCount-ClientApplication/
├── main.py                # Main entry point (GUI launcher)
├── register_user.py       # User registration logic
├── faculty_panel.py       # Faculty dashboard
├── admin_panel.py         # Admin dashboard
├── attendance_sign_in.py  # Attendance marking window
├── f_main.py              # Face recognition and camera logic
├── face_encode.py         # Face encoding utilities
├── photos/                # UI and sample images
├── user_photos/           # Uploaded user photos
├── ... (other modules)
```

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd FaceCount-ClientApplication
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   > **Note:** You may need to install additional system packages for `face_recognition` and `opencv-python` (see their documentation).

3. **Run the application:**
   ```bash
   python main.py
   ```

## Usage
- **Mark Attendance:** Launch the app and click "Mark Attendance" to scan your face and mark your attendance.
- **Admin Login:** Click "Admin" to access the admin panel for user and attendance management.
- **Faculty Login:** Click "Faculty" to access the faculty panel.
- **Register Users:** Use the registration window to add new students or faculty with their details and photo.

## Dependencies
- Python 3.10+
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (usually included with Python)
- [Pillow](https://python-pillow.org/)
- [requests](https://docs.python-requests.org/)
- [numpy](https://numpy.org/)
- [opencv-python](https://pypi.org/project/opencv-python/)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [cryptography](https://cryptography.io/)

## Notes
- User photos well be stored in the `user_photos/` directory.
- UI images are stored in the `photos/` directory.
- Attendance and user data are managed via CSV and encrypted files.

## License
This project is for academic and demonstration purposes. 