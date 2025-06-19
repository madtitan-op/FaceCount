import React from 'react';
import { Box, Typography } from '@mui/material';

interface ServerStatusProps {
    isServerDown: boolean;
}

const ServerStatus: React.FC<ServerStatusProps> = ({ isServerDown }) => {
    if (!isServerDown) return null;

    return (
        <Box
            sx={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                backgroundColor: 'error.main',
                color: 'white',
                padding: 2,
                textAlign: 'center',
                zIndex: 9999,
                animation: 'pulse 2s infinite',
                '@keyframes pulse': {
                    '0%': {
                        opacity: 1,
                    },
                    '50%': {
                        opacity: 0.7,
                    },
                    '100%': {
                        opacity: 1,
                    },
                },
            }}
        >
            <Typography
                variant="h6"
                sx={{
                    fontWeight: 'bold',
                    textTransform: 'uppercase',
                    letterSpacing: '2px',
                }}
            >
                Server Unreachable
            </Typography>
        </Box>
    );
};

export default ServerStatus; 