// src/pages/FacultyLogin.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Container,
    Paper,
    TextField,
    Button,
    Typography,
    Box,
    Alert,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';

const FacultyLogin: React.FC = () => {
    const [userid, setUserid] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useAuth();  // uses same login API
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await login(userid, password); // Same API: /api/auth/login
            navigate('/faculty-dashboard'); // ✅ Make sure this page exists
        } catch (err) {
            setError('Invalid user ID or password');
        }
    };

    return (
        <Box sx={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: 'linear-gradient(135deg, #00c6ff 0%, #0072ff 100%)',
        }}>
            <Container component="main" maxWidth="xs">
                <Paper elevation={24} sx={{ padding: 4, display: 'flex', flexDirection: 'column', alignItems: 'center', borderRadius: '20px' }}>
                    <Typography component="h1" variant="h5" sx={{ mb: 3, fontWeight: 'bold' }}>
                        Faculty Login
                    </Typography>
                    {error && <Alert severity="error" sx={{ mt: 2, width: '100%', borderRadius: '10px' }}>{error}</Alert>}
                    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1, width: '100%' }}>
                        <TextField fullWidth required label="User ID" value={userid} onChange={(e) => setUserid(e.target.value)} />
                        <TextField fullWidth required type="password" label="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                        <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, height: '50px', borderRadius: '10px' }}>
                            Sign In
                        </Button>
                    </Box>
                </Paper>
            </Container>
        </Box>
    );
};

export default FacultyLogin;
