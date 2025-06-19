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

const AdminLogin: React.FC = () => {
    const [userid, setUserid] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await login(userid, password); // This should call /api/auth/login
            navigate('/admin-dashboard');
        } catch (err) {
            setError('Invalid user ID or password');
        }
    };

    return (
        <Box sx={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg, #f7971e 0%, #ffd200 100%)' }}>
            <Container component="main" maxWidth="xs">
                <Paper elevation={24} sx={{ padding: 4, display: 'flex', flexDirection: 'column', alignItems: 'center', borderRadius: '20px' }}>
                    <Typography component="h1" variant="h5" sx={{ mb: 3, fontWeight: 'bold' }}>
                        Admin Login
                    </Typography>
                    {error && (
                        <Alert severity="error" sx={{ mt: 2, width: '100%', borderRadius: '10px' }}>{error}</Alert>
                    )}
                    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1, width: '100%' }}>
                        <TextField margin="normal" required fullWidth id="userid" label="User ID" name="userid" autoComplete="userid" autoFocus value={userid} onChange={(e) => setUserid(e.target.value)} />
                        <TextField margin="normal" required fullWidth name="password" label="Password" type="password" id="password" autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} />
                        <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2, height: '50px', borderRadius: '10px' }}>
                            Sign In
                        </Button>
                    </Box>
                </Paper>
            </Container>
        </Box>
    );
};

export default AdminLogin;
