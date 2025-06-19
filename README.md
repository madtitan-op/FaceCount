# FaceCount - Face Recognition Attendance System

FaceCount is a comprehensive attendance management system leveraging facial recognition technology. It consists of three main components:

- **FaceCount-ClientApplication**: A Python/Tkinter desktop app for face-based attendance and user management.
- **FaceCount-WebUI**: A modern React dashboard for students, faculty, and admins to view/manage attendance and profiles.
- **FaceCount-Backend**: A Spring Boot REST API backend with PostgreSQL for secure data storage and management.

---

## Features
- Face recognition-based attendance marking
- Role-based dashboards (Admin, Faculty, Student)
- User registration and management
- Attendance calendar and trends visualization
- Secure authentication (JWT)
- Encrypted data handling
- Responsive, modern UI

---

## Project Structure
```
FaceCount/
├── FaceCount-ClientApplication/   # Python/Tkinter desktop app
├── FaceCount-WebUI/               # React/TypeScript web dashboard
├── FaceCount-Backend/             # Spring Boot backend API
```

---

## Getting Started
For installation and setup instructions, please refer to the README file in each respective subfolder:

- **FaceCount-ClientApplication/README.md**
- **FaceCount-WebUI/README.md**
- **FaceCount-Backend/README.md**

Each README provides detailed prerequisites, installation steps, and usage instructions for that component.

---

## Usage Overview
- **Mark Attendance:** Use the desktop app to scan faces and mark attendance.
- **Web Dashboard:** Log in as Admin, Faculty, or Student to view/manage attendance and profiles.
- **API:** Backend provides REST endpoints for all data operations.

---

## Notes
- Ensure all three components are running for full functionality.
- For demo/testing, use the provided dummy data or register new users via the app.

---

## License
This project is for academic and demonstration purposes only. 