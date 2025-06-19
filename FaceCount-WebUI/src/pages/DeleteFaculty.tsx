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
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    Card,
    CardContent,
    Grid
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

const DeleteFaculty: React.FC = () => {
    const [facultyId, setFacultyId] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);
    const [openDialog, setOpenDialog] = useState(false);
    const [facultyDetails, setFacultyDetails] = useState<FacultyDetails | null>(null);
    const [loadingDetails, setLoadingDetails] = useState(false);
    const navigate = useNavigate();

    const fetchFacultyDetails = async (id: string) => {
        setLoadingDetails(true);
        setError(null);
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('No authentication token found');
            }

            const response = await axios.get(
                `http://localhost:8080/api/faculty/admin/details/$facultyId}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );
            setFacultyDetails(response.data);
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
        }
    }, [facultyId]);

    const handleDelete = async () => {
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

            const response = await axios.delete(
                `http://localhost:8080/api/faculty/admin/delete/${facultyId}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            if (response.status === 200) {
                setSuccess(true);
                setOpenDialog(false);
                setTimeout(() => {
                    navigate('/faculty-dashboard');
                }, 2000);
            }
        } catch (err: any) {
            console.error('Error deleting faculty:', err);
            if (err.response) {
                setError(err.response.data.message || 'Failed to delete faculty');
            } else {
                setError('Failed to delete faculty. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!facultyId) {
            setError('Please enter a faculty ID');
            return;
        }
        if (!facultyDetails) {
            setError('Please enter a valid faculty ID');
            return;
        }
        setOpenDialog(true);
    };

    return (
        <Container maxWidth="sm" sx={{ mt: 4 }}>
            <Paper elevation={3} sx={{ p: 4, borderRadius: 2 }}>
                <Typography variant="h4" gutterBottom sx={{ color: '#d32f2f', fontWeight: 'bold', textAlign: 'center' }}>
                    Delete Faculty
                </Typography>

                {error && (
                    <Alert severity="error" sx={{ mb: 3 }}>
                        {error}
                    </Alert>
                )}

                {success && (
                    <Alert severity="success" sx={{ mb: 3 }}>
                        Faculty deleted successfully! Redirecting to dashboard...
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
                        <Card sx={{ mb: 3, backgroundColor: '#f5f5f5' }}>
                            <CardContent>
                                <Typography variant="h6" gutterBottom>
                                    Faculty Details
                                </Typography>
                                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                                    <Typography><strong>Name:</strong> {facultyDetails.name}</Typography>
                                    <Typography><strong>Email:</strong> {facultyDetails.email}</Typography>
                                    <Typography><strong>Department:</strong> {facultyDetails.department}</Typography>
                                    <Typography><strong>Role:</strong> {facultyDetails.role}</Typography>
                                </Box>
                            </CardContent>
                        </Card>
                    ) : null}

                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        disabled={loading || success || !facultyDetails}
                        sx={{
                            height: 48,
                            fontSize: '1.1rem',
                            backgroundColor: '#d32f2f',
                            '&:hover': {
                                backgroundColor: '#b71c1c',
                            },
                        }}
                    >
                        {loading ? <CircularProgress size={24} color="inherit" /> : 'Delete Faculty'}
                    </Button>
                </Box>

                <Dialog 
                    open={openDialog} 
                    onClose={() => !loading && setOpenDialog(false)}
                    aria-labelledby="delete-dialog-title"
                >
                    <DialogTitle id="delete-dialog-title">Confirm Deletion</DialogTitle>
                    <DialogContent>
                        <Typography>
                            Are you sure you want to delete faculty member {facultyDetails?.name}? This action cannot be undone.
                        </Typography>
                    </DialogContent>
                    <DialogActions>
                        <Button 
                            onClick={() => setOpenDialog(false)} 
                            color="primary"
                            disabled={loading}
                        >
                            Cancel
                        </Button>
                        <Button 
                            onClick={handleDelete} 
                            color="error" 
                            variant="contained"
                            disabled={loading}
                        >
                            {loading ? <CircularProgress size={24} color="inherit" /> : 'Delete'}
                        </Button>
                    </DialogActions>
                </Dialog>
            </Paper>
        </Container>
    );
};

export default DeleteFaculty; 