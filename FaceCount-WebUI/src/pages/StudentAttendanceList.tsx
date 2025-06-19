import React, { useEffect, useState } from 'react';
import {
    Container,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    CircularProgress,
    Box,
    Alert,
    TextField,
    Button
} from '@mui/material';
import axios from 'axios';

interface AttendanceRecord {
    userId: number;
    date: string;
    status: string;
}

const StudentAttendanceList: React.FC = () => {
    const [attendanceData, setAttendanceData] = useState<AttendanceRecord[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [selectedDate, setSelectedDate] = useState(new Date());

    const fetchAttendance = async (date: Date) => {
        setLoading(true);
        setError(null);
        try {
            const day = date.getDate();
            const month = date.getMonth() + 1;
            const year = date.getFullYear();

            const token = localStorage.getItem('token');
            const response = await axios.get(
                `http://localhost:8080/api/attendance/fetch/${day}/${month}/${year}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );
            setAttendanceData(response.data);
        } catch (err) {
            setError('Failed to fetch attendance records.');
            console.error('Error fetching attendance:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAttendance(selectedDate);
    }, [selectedDate]);

    const handleDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSelectedDate(new Date(event.target.value));
    };

    const handleRefresh = () => {
        fetchAttendance(selectedDate);
    };

    return (
        <Container maxWidth="lg" sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom sx={{ color: '#1976d2', fontWeight: 'bold' }}>
                Attendance Records
            </Typography>

            <Box sx={{ mb: 4, display: 'flex', gap: 2, alignItems: 'center' }}>
                <TextField
                    type="date"
                    label="Select Date"
                    value={selectedDate.toISOString().split('T')[0]}
                    onChange={handleDateChange}
                    InputLabelProps={{ shrink: true }}
                    sx={{ flexGrow: 1 }}
                />
                <Button
                    variant="contained"
                    onClick={handleRefresh}
                    disabled={loading}
                    sx={{
                        height: 56,
                        px: 4,
                        background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
                        '&:hover': {
                            background: 'linear-gradient(45deg, #1976D2 30%, #00BCD4 90%)',
                        },
                    }}
                >
                    Refresh
                </Button>
            </Box>

            {loading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', mt: 5 }}>
                    <CircularProgress />
                </Box>
            ) : error ? (
                <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>
            ) : (
                <TableContainer component={Paper} sx={{ mt: 2, boxShadow: 3 }}>
                    <Table>
                        <TableHead>
                            <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                                <TableCell><b>User ID</b></TableCell>
                                <TableCell><b>Date</b></TableCell>
                                <TableCell><b>Status</b></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {attendanceData.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={3} align="center">
                                        No attendance records found for selected date
                                    </TableCell>
                                </TableRow>
                            ) : (
                                attendanceData.map((record, index) => (
                                    <TableRow key={index} hover>
                                        <TableCell>{record.userId}</TableCell>
                                        <TableCell>{record.date}</TableCell>
                                        <TableCell>
                                            <Typography
                                                sx={{
                                                    color: record.status === 'PRESENT' ? 'green' : 'red',
                                                    fontWeight: 'bold'
                                                }}
                                            >
                                                {record.status}
                                            </Typography>
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}
        </Container>
    );
};

export default StudentAttendanceList;
