import React, { useState, useEffect } from 'react';
import {
    Container,
    Paper,
    Typography,
    TextField,
    Button,
    Box,
    Alert,
    CircularProgress,
    MenuItem
} from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

interface FacultyDetails {
    id: number;
    name: string;
    email: string;
    department: string;
    role: string;
}

const departments = [
    'CSE',
    'ME',
    'EE',
    'CE',
    'IT',
    'ECE'
];

const roles = [
    'ADMIN',
    'FACULTY'
];

const UpdateFaculty: React.FC = () => {
    const navigate = useNavigate();
    const [facultyId, setFacultyId] = useState('');
    const [facultyDetails, setFacultyDetails] = useState<FacultyDetails | null>(null);
    const [loading, setLoading] = useState(false);
    const [loadingDetails, setLoadingDetails] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        department: '',
        role: '',
        password: ''
    });

    const fetchFacultyDetails = async (id: string) => {
        setLoadingDetails(true);
        setError(null);
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('No authentication token found');
            }

            const response = await axios.get(
                `http://localhost:8080/api/faculty/admin/details/${id}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );
            setFacultyDetails(response.data);
            setFormData({
                name: response.data.name,
                email: response.data.email,
                department: response.data.department,
                role: response.data.role,
                password: ''
            });
        } catch (err: any) {
            console.error('Error fetching faculty details:', err);
            setFacultyDetails(null);
            if (err.response) {
                setError(err.response.data.message || 'Failed to fetch faculty details');
            } else {
                setError('Failed to fetch faculty details. Please try again.');
            }
        } finally {
            setLoadingDetails(false);
        }
    };

    useEffect(() => {
        if (facultyId) {
            const timer = setTimeout(() => {
                fetchFacultyDetails(facultyId);
            }, 500);

            return () => clearTimeout(timer);
        } else {
            setFacultyDetails(null);
            setFormData({
                name: '',
                email: '',
                department: '',
                role: '',
                password: ''
            });
        }
    }, [facultyId]);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!facultyId) {
            setError('Please enter a faculty ID');
            return;
        }

        setLoading(true);
        setError(null);
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('No authentication token found');
            }

            const requestData = {
                faculty_id: parseInt(facultyId),
                ...formData
            };

            const response = await axios.put(
                `http://localhost:8080/api/faculty/admin/update/${facultyId}`,
                requestData,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                }
            );

            if (response.status === 200) {
                setSuccess(true);
                setTimeout(() => {
                    navigate('/faculty-dashboard');
                }, 2000);
            }
        } catch (err: any) {
            console.error('Error updating faculty:', err);
            if (err.response) {
                setError(err.response.data.message || 'Failed to update faculty');
            } else {
                setError('Failed to update faculty. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <Container maxWidth="md" sx={{ mt: 4 }}>
            <Paper elevation={3} sx={{ p: 4, borderRadius: 2 }}>
                <Typography variant="h4" gutterBottom sx={{ color: '#1976d2', fontWeight: 'bold', textAlign: 'center' }}>
                    Update Faculty
                </Typography>

                {error && (
                    <Alert severity="error" sx={{ mb: 3 }}>
                        {error}
                    </Alert>
                )}

                {success && (
                    <Alert severity="success" sx={{ mb: 3 }}>
                        Faculty updated successfully! Redirecting to dashboard...
                    </Alert>
                )}

                <Box component="form" onSubmit={handleSubmit}>
                    <TextField
                        fullWidth
                        label="Faculty ID"
                        value={facultyId}
                        onChange={(e) => {
                            setFacultyId(e.target.value);
                            setError(null);
                        }}
                        required
                        margin="normal"
                        sx={{ mb: 3 }}
                        error={!!error}
                        helperText={error}
                    />

                    {loadingDetails ? (
                        <Box display="flex" justifyContent="center" my={3}>
                            <CircularProgress />
                        </Box>
                    ) : facultyDetails ? (
                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                            <TextField
                                fullWidth
                                label="Name"
                                name="name"
                                value={formData.name}
                                onChange={handleInputChange}
                                required
                            />
                            <TextField
                                fullWidth
                                label="Email"
                                name="email"
                                type="email"
                                value={formData.email}
                                onChange={handleInputChange}
                                required
                            />
                            <TextField
                                fullWidth
                                label="Password"
                                name="password"
                                type="password"
                                value={formData.password}
                                onChange={handleInputChange}
                                required
                                helperText="Enter new password to update"
                            />
                            <Box sx={{ display: 'flex', gap: 3 }}>
                                <TextField
                                    fullWidth
                                    select
                                    label="Department"
                                    name="department"
                                    value={formData.department}
                                    onChange={handleInputChange}
                                    required
                                >
                                    {departments.map((dept) => (
                                        <MenuItem key={dept} value={dept}>
                                            {dept}
                                        </MenuItem>
                                    ))}
                                </TextField>
                                <TextField
                                    fullWidth
                                    select
                                    label="Role"
                                    name="role"
                                    value={formData.role}
                                    onChange={handleInputChange}
                                    required
                                >
                                    {roles.map((role) => (
                                        <MenuItem key={role} value={role}>
                                            {role}
                                        </MenuItem>
                                    ))}
                                </TextField>
                            </Box>
                        </Box>
                    ) : null}

                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        disabled={loading || success || !facultyDetails}
                        sx={{
                            mt: 3,
                            height: 48,
                            fontSize: '1.1rem',
                            background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                            '&:hover': {
                                background: 'linear-gradient(45deg, #1976D2 30%, #00BCD4 90%)',
                            },
                        }}
                    >
                        {loading ? <CircularProgress size={24} color="inherit" /> : 'Update Faculty'}
                    </Button>
                </Box>
            </Paper>
        </Container>
    );
};

export default UpdateFaculty; 