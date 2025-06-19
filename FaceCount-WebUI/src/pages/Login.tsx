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

const Login: React.FC = () => {
    const [userid, setUserid] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await login(userid, password);
            navigate('/dashboard');
        } catch (err) {
            setError('Invalid user ID or password');
        }
    };

    return (
        <Box
            sx={{
                minHeight: '100vh',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: 'linear-gradient(135deg, #1a237e 0%, #0d47a1 100%)',
                position: 'relative',
                overflow: 'hidden',
                '&::before': {
                    content: '""',
                    position: 'absolute',
                    width: '200%',
                    height: '200%',
                    background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%)',
                    animation: 'rotate 20s linear infinite',
                },
                '@keyframes rotate': {
                    '0%': {
                        transform: 'rotate(0deg)',
                    },
                    '100%': {
                        transform: 'rotate(360deg)',
                    },
                },
            }}
        >
            <Container component="main" maxWidth="xs">
                <Paper
                    elevation={24}
                    sx={{
                        padding: 4,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        background: 'rgba(255, 255, 255, 0.9)',
                        backdropFilter: 'blur(10px)',
                        borderRadius: '20px',
                        transform: 'perspective(1000px) rotateX(5deg)',
                        transition: 'transform 0.3s ease',
                        '&:hover': {
                            transform: 'perspective(1000px) rotateX(0deg)',
                        },
                        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
                    }}
                >
                    <Box
                        sx={{
                            width: '100px',
                            height: '100px',
                            borderRadius: '50%',
                            background: 'linear-gradient(45deg, #1a237e, #0d47a1)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            marginBottom: 3,
                            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)',
                            transform: 'translateZ(20px)',
                        }}
                    >
                        <Typography
                            variant="h4"
                            sx={{
                                color: 'white',
                                fontWeight: 'bold',
                            }}
                        >
                            👤
                        </Typography>
                    </Box>

                    <Typography
                        component="h1"
                        variant="h5"
                        sx={{
                            mb: 3,
                            fontWeight: 'bold',
                            background: 'linear-gradient(45deg, #1a237e, #0d47a1)',
                            WebkitBackgroundClip: 'text',
                            WebkitTextFillColor: 'transparent',
                        }}
                    >
                        User Login
                    </Typography>

                    {error && (
                        <Alert
                            severity="error"
                            sx={{
                                mt: 2,
                                width: '100%',
                                borderRadius: '10px',
                                boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
                            }}
                        >
                            {error}
                        </Alert>
                    )}

                    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1, width: '100%' }}>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="userid"
                            label="User ID"
                            name="userid"
                            autoComplete="userid"
                            autoFocus
                            value={userid}
                            onChange={(e) => setUserid(e.target.value)}
                            sx={{
                                '& .MuiOutlinedInput-root': {
                                    borderRadius: '10px',
                                    transition: 'transform 0.2s ease',
                                    '&:hover': {
                                        transform: 'translateY(-2px)',
                                    },
                                },
                            }}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            sx={{
                                '& .MuiOutlinedInput-root': {
                                    borderRadius: '10px',
                                    transition: 'transform 0.2s ease',
                                    '&:hover': {
                                        transform: 'translateY(-2px)',
                                    },
                                },
                            }}
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{
                                mt: 3,
                                mb: 2,
                                height: '50px',
                                borderRadius: '10px',
                                background: 'linear-gradient(45deg, #1a237e, #0d47a1)',
                                boxShadow: '0 4px 15px rgba(0, 0, 0, 0.2)',
                                transition: 'all 0.3s ease',
                                '&:hover': {
                                    transform: 'translateY(-2px)',
                                    boxShadow: '0 6px 20px rgba(0, 0, 0, 0.3)',
                                },
                            }}
                        >
                            Sign In
                        </Button>
                    </Box>
                </Paper>
            </Container>
        </Box>
    );
};

export default Login;