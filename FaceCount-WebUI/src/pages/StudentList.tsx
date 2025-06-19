import React, { useState } from 'react';
import {
    Box,
    Container,
    Typography,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    CircularProgress,
} from '@mui/material';
import axios from 'axios';

interface Student {
    student_id: number;
    name: string;
    email: string;
    department: string;
    yop: number;
    role: string;
}

const departments = ['CSE', 'ECE', 'ME', 'CE', 'EE', 'IT'];

const StudentList: React.FC = () => {
    const [selectedDept, setSelectedDept] = useState('');
    const [students, setStudents] = useState<Student[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const fetchStudents = async (department: string) => {
        setLoading(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(
                `http://localhost:8080/api/student/admin/dept/${department}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            setStudents(response.data);
        } catch (err) {
            setError('Failed to fetch students');
            console.error('Error fetching students:', err);
        }
        setLoading(false);
    };

    const handleDepartmentChange = (event: any) => {
        const dept = event.target.value;
        setSelectedDept(dept);
        if (dept) {
            fetchStudents(dept);
        }
    };

    return (
        <Container maxWidth="lg" sx={{ mt: 8, mb: 8 }}>
            <Paper
                elevation={10}
                sx={{
                    p: 4,
                    borderRadius: '30px',
                    background: 'linear-gradient(135deg, rgba(255,255,255,0.8), rgba(240,248,255,0.9))',
                    backdropFilter: 'blur(15px)',
                    boxShadow: '0px 20px 40px rgba(0, 0, 0, 0.2)',
                    border: '1px solid rgba(255,255,255,0.3)',
                    transition: 'all 0.3s ease-in-out',
                }}
            >
                <Typography
                    variant="h3"
                    gutterBottom
                    sx={{
                        fontWeight: 'bold',
                        textAlign: 'center',
                        color: '#0d47a1',
                        letterSpacing: 1.5,
                        mb: 5,
                        textShadow: '1px 2px 2px rgba(0,0,0,0.15)',
                    }}
                >
                    🎓 Student List
                </Typography>

                <FormControl fullWidth sx={{ mb: 5 }}>
                    <InputLabel sx={{ fontWeight: 600 }}>Select Department</InputLabel>
                    <Select
                        value={selectedDept}
                        label="Select Department"
                        onChange={handleDepartmentChange}
                        sx={{
                            backgroundColor: '#ffffffcc',
                            borderRadius: 2,
                            boxShadow: 'inset 0 0 5px rgba(0,0,0,0.1)',
                        }}
                    >
                        {departments.map((dept) => (
                            <MenuItem key={dept} value={dept}>
                                {dept}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                {error && (
                    <Typography
                        color="error"
                        sx={{
                            mb: 3,
                            fontWeight: 600,
                            textAlign: 'center',
                        }}
                    >
                        {error}
                    </Typography>
                )}

                {loading ? (
                    <Box display="flex" justifyContent="center" alignItems="center" mt={5}>
                        <CircularProgress size={50} color="primary" />
                    </Box>
                ) : (
                    <TableContainer
                        component={Paper}
                        sx={{
                            borderRadius: '20px',
                            overflow: 'hidden',
                            boxShadow: '0px 8px 24px rgba(0,0,0,0.1)',
                        }}
                    >
                        <Table>
                            <TableHead>
                                <TableRow
                                    sx={{
                                        background: 'linear-gradient(45deg, #3949ab, #1e88e5)',
                                    }}
                                >
                                    {['ID', 'Name', 'Email', 'Department', 'YOP', 'Role'].map((header) => (
                                        <TableCell
                                            key={header}
                                            sx={{
                                                color: '#ffffff',
                                                fontWeight: 700,
                                                fontSize: '15px',
                                            }}
                                        >
                                            {header}
                                        </TableCell>
                                    ))}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {students.map((student, index) => (
                                    <TableRow
                                        key={student.student_id}
                                        sx={{
                                            backgroundColor: index % 2 === 0 ? '#fdfdfd' : '#eef6ff',
                                            transition: '0.3s',
                                            '&:hover': {
                                                backgroundColor: '#dbefff',
                                                transform: 'scale(1.01)',
                                                boxShadow: '0 2px 10px rgba(0,0,0,0.08)',
                                            },
                                        }}
                                    >
                                        <TableCell>{student.student_id}</TableCell>
                                        <TableCell>{student.name}</TableCell>
                                        <TableCell>{student.email}</TableCell>
                                        <TableCell>{student.department}</TableCell>
                                        <TableCell>{student.yop}</TableCell>
                                        <TableCell>{student.role}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                )}
            </Paper>
        </Container>
    );
};

export default StudentList;
