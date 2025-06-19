import React, { useEffect, useState } from 'react';
import { Box, Button, Typography, Paper, CircularProgress, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

interface FacultyDetails {
    name: string;
    email: string;
    role: string;
    department: string;
}

const FacultyDashboard: React.FC = () => {
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

    const handleUpdateFaculty = () => {
        navigate('/faculty/update');
    };

    const handleDeleteFaculty = () => {
        navigate('/faculty/delete');
    };

    const handleShowAttendance = () => {
        navigate('/faculty/attendance');
    };

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <Typography color="error">{error}</Typography>
            </Box>
        );
    }

    return (
        <Box
            sx={{
                minHeight: '100vh',
                background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
                py: 8,
            }}
        >
            <Container maxWidth="lg">
                <Paper
                    elevation={3}
                    sx={{
                        p: 4,
                        borderRadius: 2,
                        background: 'rgba(255, 255, 255, 0.9)',
                        backdropFilter: 'blur(10px)',
                    }}
                >
                    <Typography
                        variant="h4"
                        gutterBottom
                        sx={{
                            textAlign: 'center',
                            color: '#1976d2',
                            fontWeight: 'bold',
                            mb: 4,
                        }}
                    >
                        Welcome Faculty {facultyDetails?.name}
                    </Typography>

                    <Box
                        sx={{
                            display: 'grid',
                            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                            gap: 3,
                            mt: 4,
                        }}
                    >
                        <Button
                            variant="contained"
                            onClick={handleUpdateFaculty}
                            sx={{
                                height: 100,
                                fontSize: '1.2rem',
                                background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                                '&:hover': {
                                    background: 'linear-gradient(45deg, #1976D2 30%, #00BCD4 90%)',
                                },
                            }}
                        >
                            Update Faculty
                        </Button>

                        <Button
                            variant="contained"
                            onClick={handleDeleteFaculty}
                            sx={{
                                height: 100,
                                fontSize: '1.2rem',
                                background: 'linear-gradient(45deg, #FF5252 30%, #FF4081 90%)',
                                '&:hover': {
                                    background: 'linear-gradient(45deg, #D32F2F 30%, #C2185B 90%)',
                                },
                            }}
                        >
                            Delete Faculty
                        </Button>

                        <Button
                            variant="contained"
                            onClick={handleShowAttendance}
                            sx={{
                                height: 100,
                                fontSize: '1.2rem',
                                background: 'linear-gradient(45deg, #4CAF50 30%, #8BC34A 90%)',
                                '&:hover': {
                                    background: 'linear-gradient(45deg, #388E3C 30%, #689F38 90%)',
                                },
                            }}
                        >
                            Show Attendance
                        </Button>
                    </Box>
                </Paper>
            </Container>
        </Box>
    );
};

export default FacultyDashboard;
