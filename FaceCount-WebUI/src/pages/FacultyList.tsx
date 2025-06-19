import React, { useState } from 'react';
import {
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
    Box,
    CircularProgress,
} from '@mui/material';
import axios from 'axios';

interface Faculty {
    faculty_id: number;
    name: string;
    email: string;
    department: string;
    role: string;
}

const departments = ['CSE', 'ECE', 'ME', 'CE', 'EE', 'IT'];

const FacultyList: React.FC = () => {
    const [selectedDept, setSelectedDept] = useState('');
    const [facultyList, setFacultyList] = useState<Faculty[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const fetchFaculty = async (department: string) => {
        setLoading(true);
        setError('');
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`http://localhost:8080/api/faculty/admin/dept/${department}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            console.log('API Response:', response.data);
            setFacultyList(response.data);
        } catch (err) {
            setError('Failed to fetch faculty. Please try again later.');
            console.error('Error fetching faculty:', err);
        }
        setLoading(false);
    };

    const handleDepartmentChange = (event: any) => {
        const dept = event.target.value;
        setSelectedDept(dept);
        if (dept) {
            fetchFaculty(dept);
        }
    };

    return (
        <Container maxWidth="lg" sx={{ mt: 6, mb: 6 }}>
            <Paper
                elevation={4}
                sx={{
                    p: 4,
                    borderRadius: 3,
                    backgroundColor: '#fefefe',
                    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.1)',
                }}
            >
                <Typography
                    variant="h4"
                    gutterBottom
                    sx={{
                        mb: 4,
                        fontWeight: 'bold',
                        color: '#333',
                        textAlign: 'center',
                        letterSpacing: 1,
                    }}
                >
                    Faculty List
                </Typography>

                <Box sx={{ mb: 4 }}>
                    <FormControl fullWidth variant="outlined">
                        <InputLabel>Department</InputLabel>
                        <Select
                            value={selectedDept}
                            onChange={handleDepartmentChange}
                            label="Department"
                        >
                            {departments.map((dept) => (
                                <MenuItem key={dept} value={dept}>
                                    {dept}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Box>

                {error && (
                    <Typography color="error" sx={{ mb: 2, textAlign: 'center' }}>
                        {error}
                    </Typography>
                )}

                {loading ? (
                    <Box display="flex" justifyContent="center" alignItems="center" mt={3}>
                        <CircularProgress />
                    </Box>
                ) : (
                    facultyList.length > 0 ? (
                        <TableContainer component={Paper} sx={{ borderRadius: 2, boxShadow: 2 }}>
                            <Table>
                                <TableHead sx={{ backgroundColor: '#1976d2' }}>
                                    <TableRow>
                                        <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Faculty ID</TableCell>
                                        <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Name</TableCell>
                                        <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Email</TableCell>
                                        <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Department</TableCell>
                                        <TableCell sx={{ color: '#fff', fontWeight: 'bold' }}>Role</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {facultyList.map((faculty) => (
                                        <TableRow
                                            key={faculty.faculty_id}
                                            sx={{
                                                '&:hover': {
                                                    backgroundColor: '#f5f5f5',
                                                    cursor: 'pointer',
                                                },
                                            }}
                                        >
                                            <TableCell>{faculty.faculty_id}</TableCell>
                                            <TableCell>{faculty.name}</TableCell>
                                            <TableCell>{faculty.email}</TableCell>
                                            <TableCell>{faculty.department}</TableCell>
                                            <TableCell>{faculty.role}</TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    ) : selectedDept ? (
                        <Typography textAlign="center" color="text.secondary" mt={3}>
                            No faculty members found in {selectedDept} department.
                        </Typography>
                    ) : null
                )}
            </Paper>
        </Container>
    );
};

export default FacultyList;
