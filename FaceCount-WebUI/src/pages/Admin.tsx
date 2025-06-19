import { Box, Container, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

interface ButtonProps {
    label: string;
    colors: string[];
    orbGradient: string;
    navigateTo: string;
}

const GradientButton = ({ label, colors, orbGradient, navigateTo }: ButtonProps) => {
    const navigate = useNavigate();
    return (
        <Box
            onClick={() => navigate(navigateTo)}
            sx={{
                background: `linear-gradient(to right, ${colors[0]}, ${colors[1]})`,
                borderRadius: '60px',
                display: 'flex',
                alignItems: 'center',
                height: 80,
                fontSize: '1.5rem',
                fontWeight: 'bold',
                color: '#fff',
                cursor: 'pointer',
                boxShadow: `0 10px 20px ${colors[2]}`,
                '&:hover': {
                    transform: 'scale(1.03)',
                    boxShadow: `0 12px 24px ${colors[3]}`,
                },
                transition: 'all 0.3s ease',
                px: 3,
            }}
        >
            <Box
                sx={{
                    width: 55,
                    height: 55,
                    borderRadius: '50%',
                    background: orbGradient,
                    boxShadow: '0 0 12px rgba(255,255,255,0.3)',
                    mr: 2,
                }}
            />
            {label}
        </Box>
    );
};

const Admin = () => {
    const navigate = useNavigate();

    return (
        <Box
            sx={{
                minHeight: '100vh',
                backgroundColor: '#0e0e0e',
                color: '#fff',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                px: 3,
            }}
        >
            <Container maxWidth="lg">
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    {/* Left Side Text */}
                    <Box sx={{ flex: 1 }}>
                        <Typography
                            variant="h2"
                            component="h1"
                            sx={{
                                fontWeight: 'bold',
                                mb: 3,
                                lineHeight: 1.2,
                                fontSize: {
                                    xs: '2rem',
                                    sm: '3rem',
                                    md: '3rem',
                                },
                            }}
                        >
                            <span style={{ color: '#fff' }}>Facecount A Face</span> <br />
                            <span style={{ color: '#fff' }}> Recognization based attendance systems.</span>
                        </Typography>
                        <Typography variant="subtitle1" sx={{ color: '#ccc', mb: 4 }}>
                           FaceCount redefines classroom presence with instant, touchless facial recognition for modern education.
                        </Typography>
                        <Box
                            sx={{
                                display: 'inline-block',
                                border: '1px solid #fff',
                                color: '#fff',
                                px: 3,
                                py: 1,
                                borderRadius: '50px',
                                cursor: 'pointer',
                                '&:hover': {
                                    backgroundColor: '#fff',
                                    color: '#000',
                                },
                            }}
                        >
                            Let's fetch your details
                        </Box>
                    </Box>

                    {/* Right Side Panels */}
                    <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 4 }}>
                        <Box
                            onClick={() => navigate('/login')}
                            sx={{
                                background: 'linear-gradient(to right, #ff512f, #f09819)',
                                borderRadius: '60px',
                                display: 'flex',
                                alignItems: 'center',
                                height: 80,
                                fontSize: '1.5rem',
                                fontWeight: 'bold',
                                color: '#fff',
                                cursor: 'pointer',
                                boxShadow: '0 10px 20px rgba(255, 81, 47, 0.5)',
                                '&:hover': {
                                    transform: 'scale(1.03)',
                                    boxShadow: '0 12px 24px rgba(255, 81, 47, 0.6)',
                                },
                                transition: 'all 0.3s ease',
                                px: 3,
                            }}
                        >
                            <Box
                                sx={{
                                    width: 55,
                                    height: 55,
                                    borderRadius: '50%',
                                    background: 'radial-gradient(circle at 30% 30%, #ffcc80, #ff5722)',
                                    boxShadow: '0 0 12px rgba(255, 81, 47, 0.5)',
                                    mr: 2,
                                }}
                            />
                            Student
                        </Box>

                        <Box
                            onClick={() => navigate('/admin-login')}
                            sx={{
                                background: 'linear-gradient(to right, #f7971e, #ffd200)',
                                borderRadius: '60px',
                                display: 'flex',
                                alignItems: 'center',
                                height: 80,
                                fontSize: '1.5rem',
                                fontWeight: 'bold',
                                color: '#fff',
                                cursor: 'pointer',
                                boxShadow: '0 10px 20px rgba(255, 210, 0, 0.5)',
                                '&:hover': {
                                    transform: 'scale(1.03)',
                                    boxShadow: '0 12px 24px rgba(255, 210, 0, 0.6)',
                                },
                                transition: 'all 0.3s ease',
                                px: 3,
                            }}
                        >
                            <Box
                                sx={{
                                    width: 55,
                                    height: 55,
                                    borderRadius: '50%',
                                    background: 'radial-gradient(circle at 30% 30%, #fff176, #f57f17)',
                                    boxShadow: '0 0 12px rgba(255, 215, 0, 0.6)',
                                    mr: 2,
                                }}
                            />
                            Admin
                        </Box>

                        <Box
                            onClick={() => navigate('/faculty-login')}
                            sx={{
                                background: 'linear-gradient(to right, #00c6ff, #0072ff)',
                                borderRadius: '60px',
                                display: 'flex',
                                alignItems: 'center',
                                height: 80,
                                fontSize: '1.5rem',
                                fontWeight: 'bold',
                                color: '#fff',
                                cursor: 'pointer',
                                boxShadow: '0 10px 20px rgba(0, 114, 255, 0.5)',
                                '&:hover': {
                                    transform: 'scale(1.03)',
                                    boxShadow: '0 12px 24px rgba(0, 114, 255, 0.6)',
                                },
                                transition: 'all 0.3s ease',
                                px: 3,
                            }}
                        >
                            <Box
                                sx={{
                                    width: 55,
                                    height: 55,
                                    borderRadius: '50%',
                                    background: 'radial-gradient(circle at 30% 30%, #81d4fa, #0288d1)',
                                    boxShadow: '0 0 12px rgba(0, 114, 255, 0.5)',
                                    mr: 2,
                                }}
                            />
                            Faculty
                        </Box>
                    </Box>
                </Box>
            </Container>
        </Box>
    );
};

export default Admin;
