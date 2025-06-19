# FaceCount Dashboard

A modern, role-based React UI for the FaceCount application, providing dashboards and management tools for students, faculty, and administrators. The dashboard displays attendance records, user profiles, and supports faculty management with a responsive, Material-UI powered design.

## Features

- **Role-based dashboards:** Separate dashboards for Admin, Faculty, and Student users
- **User authentication:** Secure JWT-based login for all user types
- **Profile management:** View and update user (student/faculty) profiles
- **Faculty management:** Admins can add, update, and delete faculty members
- **Student & faculty listing:** Filter and view lists by department and role
- **Attendance calendar:** Students can view monthly attendance in a calendar format
- **Attendance trends:** Visualize yearly attendance trends with charts
- **Real-time server status:** UI indicator for backend server connectivity
- **Responsive design:** Optimized for desktop and mobile with Material-UI
- **Data visualization:** Interactive charts using Recharts
- **Robust error handling:** User-friendly error and loading states throughout

## User Roles & Dashboards

- **Admin:**
  - Login via `/admin-login`
  - Access admin dashboard to manage faculty and view lists
- **Faculty:**
  - Login via `/faculty-login`
  - Access faculty dashboard, view/update/delete profile, and manage student attendance
- **Student:**
  - Login via `/login`
  - Access student dashboard, view profile, attendance calendar, and trends

## Project Structure

```
FaceCount-WebUI/
├── public/                # Static assets
├── src/
│   ├── assets/            # Images and static files
│   ├── components/        # Reusable UI components
│   ├── contexts/          # React context providers (e.g., Auth)
│   ├── pages/             # Page-level components (Dashboards, Login, etc.)
│   ├── services/          # API and utility services
│   ├── types/             # TypeScript type definitions
│   ├── App.tsx            # Main app and routing
│   └── main.tsx           # App entry point
├── package.json           # Project metadata and dependencies
├── vite.config.ts         # Vite configuration
└── ...
```

## Technologies Used

- [React 19](https://react.dev/)
- [TypeScript](https://www.typescriptlang.org/)
- [Material-UI 7](https://mui.com/)
- [React Router 7](https://reactrouter.com/)
- [Axios](https://axios-http.com/)
- [date-fns](https://date-fns.org/)
- [Recharts](https://recharts.org/)
- [Vite](https://vitejs.dev/) (development/build)
- [ESLint](https://eslint.org/) (linting)

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- Backend server running on `localhost:8080`

## Installation

1. Clone the repository
2. Navigate to the project directory:
   ```bash
   cd FaceCount-WebUI
   ```
3. Install dependencies:
   ```bash
   npm install
   ```

## Development

To start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Building for Production

To create a production build:

```bash
npm run build
```

The built files will be in the `dist` directory.

## API Endpoints

The application uses the following API endpoints:

- `POST /api/auth/login` - User login (all roles)
- `GET /api/student/me` - Get student profile
- `GET /api/faculty/me` - Get faculty profile
- `GET /api/attendance/fetch/{month}/{year}?userId={student_id}` - Get attendance records
- `POST /api/faculty/add` - Add new faculty (admin only)
- `PUT /api/faculty/update` - Update faculty details (admin/faculty)
- `DELETE /api/faculty/delete` - Delete faculty (admin only)

## Authentication

- JWT tokens are used for authentication.
- Tokens are stored in `localStorage` and included in all API requests (except login).
- Users are redirected to the login page if authentication fails or expires.

