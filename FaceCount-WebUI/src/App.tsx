import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { subscribeToServerStatus } from './services/api';

// Page components
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Admin from './pages/Admin';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import StudentList from './pages/StudentList';
import FacultyList from './pages/FacultyList';
import FacultyLogin from './pages/FacultyLogin';
import FacultyDashboard from './pages/FacultyDashboard';
import StudentAttendanceList from './pages/StudentAttendanceList';
import DeleteFaculty from './pages/DeleteFaculty';
import UpdateFaculty from './pages/UpdateFaculty';


// Other components
import ServerStatus from './components/ServerStatus';

const theme = createTheme({
    palette: {
        primary: {
            main: '#1976d2',
        },
        secondary: {
            main: '#dc004e',
        },
        background: {
            default: '#f5f5f5',
            paper: '#ffffff',
        },
    },
    components: {
        MuiPaper: {
            styleOverrides: {
                root: {
                    backgroundColor: '#f8f9fa',
                },
            },
        },
    },
});

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const { isAuthenticated } = useAuth();
    return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

const AppContent = () => {
    const [isServerDown, setIsServerDown] = useState(false);

    useEffect(() => {
        const checkServerStatus = async () => {
            try {
                await fetch('http://localhost:8080/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ userid: '', password: '' }),
                });
                setIsServerDown(false);
            } catch {
                setIsServerDown(true);
            }
        };

        checkServerStatus();
        const unsubscribe = subscribeToServerStatus(setIsServerDown);
        return () => unsubscribe();
    }, []);

    return (
        <>
            <ServerStatus isServerDown={isServerDown} />
            <Router>
                <Routes>
                    {/* Default redirect to /admin */}
                    <Route path="/" element={<Navigate to="/admin" />} />

                    {/* General Routes */}
                    <Route path="/login" element={<Login />} />
                    <Route path="/dashboard" element={
                        <PrivateRoute>
                            <Dashboard />
                        </PrivateRoute>
                    } />

                    {/* Admin Routes */}
                    <Route path="/admin" element={<Admin />} />
                    <Route path="/admin-login" element={<AdminLogin />} />
                    <Route path="/admin-dashboard" element={<AdminDashboard />} />
                    <Route path="/admin/students" element={<StudentList />} />
                    <Route path="/admin/faculty" element={<FacultyList />} />

                    {/* Faculty Routes */}
                    <Route path="/faculty-login" element={<FacultyLogin />} />
                    <Route path="/faculty-dashboard" element={<FacultyDashboard />} />
                    <Route path="/faculty/attendance" element={<StudentAttendanceList />} />
                    <Route path="/faculty/delete" element={<DeleteFaculty />} />
                    <Route path="/faculty/update" element={<UpdateFaculty />} />
                    
                </Routes>
            </Router>
        </>
    );
};

const App = () => {
    return (
        <ThemeProvider theme={theme}>
            <AuthProvider>
                <AppContent />
            </AuthProvider>
        </ThemeProvider>
    );
};

export default App;
