import React, { useEffect, useState } from 'react';
import { Box, Button, Typography, Paper, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface FacultyDetails {
    name: string;
    email: string;
    role: string;
    department: string;
}

const AdminDashboard: React.FC = () => {
    const navigate = useNavigate();
    const [facultyDetails, setFacultyDetails] = useState<FacultyDetails | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchFacultyDetails = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get('http://localhost:8080/api/faculty/me', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                setFacultyDetails(response.data);
            } catch (err) {
                setError('Failed to fetch faculty details');
                console.error('Error fetching faculty details:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchFacultyDetails();
    }, []);

    const handleAllStudents = () => {
        navigate('/admin/students');
    };

    const handleAllFaculty = () => {
        navigate('/admin/faculty');
    };

    return (
        <Box
            sx={{
                minHeight: '100vh',
                background: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                padding: 4,
            }}
        >
            <Paper
                elevation={10}
                sx={{
                    display: 'flex',
                    width: '90%',
                    maxWidth: 1000,
                    minHeight: 450,
                    borderRadius: '30px',
                    overflow: 'hidden',
                    backdropFilter: 'blur(12px)',
                    background: 'rgba(255, 255, 255, 0.8)',
                    boxShadow: '0 20px 50px rgba(0, 0, 0, 0.2)',
                    transition: 'transform 0.3s ease',
                    '&:hover': {
                        transform: 'scale(1.01)',
                    },
                }}
            >
                {/* Left Panel: Admin Info */}
                <Box
                    sx={{
                        flex: 1,
                        p: 5,
                        background: 'linear-gradient(to bottom right, #ffffffbb, #f5f5f5cc)',
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        borderRight: '1px solid rgba(0,0,0,0.05)',
                    }}
                >
                    <Typography
                        variant="h4"
                        fontWeight={700}
                        gutterBottom
                        sx={{
                            color: '#1a237e',
                            textShadow: '1px 1px 1px rgba(0,0,0,0.1)',
                            mb: 3,
                        }}
                    >
                        👤 Admin Details
                    </Typography>
                    {loading ? (
                        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 200 }}>
                            <CircularProgress size={40} color="secondary" />
                        </Box>
                    ) : error ? (
                        <Typography color="error">{error}</Typography>
                    ) : facultyDetails ? (
                        <Box sx={{ fontSize: '1.05rem', lineHeight: 2 }}>
                            <Typography><b>Name:</b> {facultyDetails.name}</Typography>
                            <Typography><b>Email:</b> {facultyDetails.email}</Typography>
                            <Typography><b>Role:</b> {facultyDetails.role}</Typography>
                            <Typography><b>Department:</b> {facultyDetails.department}</Typography>
                        </Box>
                    ) : (
                        <Typography>No details available</Typography>
                    )}
                </Box>

                {/* Right Panel: Buttons */}
                <Box
                    sx={{
                        flex: 1,
                        p: 5,
                        display: 'flex',
                        flexDirection: 'column',
                        justifyContent: 'center',
                        alignItems: 'center',
                        background: 'radial-gradient(circle at top left, #ffcc80, #ffb74d)',
                    }}
                >
                    <Button
                        variant="contained"
                        onClick={handleAllStudents}
                        sx={{
                            width: 220,
                            height: 60,
                            fontSize: '1.2rem',
                            fontWeight: 600,
                            borderRadius: '15px',
                            background: 'linear-gradient(to right, #2196f3, #21cbf3)',
                            boxShadow: '0 6px 15px rgba(0, 0, 0, 0.2)',
                            mb: 3,
                            '&:hover': {
                                background: 'linear-gradient(to right, #1976d2, #00bcd4)',
                                transform: 'scale(1.05)',
                            },
                        }}
                    >
                        📘 All Students
                    </Button>

                    <Button
                        variant="contained"
                        onClick={handleAllFaculty}
                        sx={{
                            width: 220,
                            height: 60,
                            fontSize: '1.2rem',
                            fontWeight: 600,
                            borderRadius: '15px',
                            background: 'linear-gradient(to right, #43e97b, #38f9d7)',
                            boxShadow: '0 6px 15px rgba(0, 0, 0, 0.2)',
                            '&:hover': {
                                background: 'linear-gradient(to right, #00c853, #00e5ff)',
                                transform: 'scale(1.05)',
                            },
                        }}
                    >
                        👨‍🏫 All Faculty
                    </Button>
                </Box>
            </Paper>
        </Box>
    );
};

export default AdminDashboard;
