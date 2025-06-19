import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Box, Button } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { getStudentProfile, getAttendanceRecords, subscribeToServerStatus } from '../services/api';
import type { Student, AttendanceRecord } from '../types';
import {
    format,
    startOfDay,
    isSameDay,
    parseISO,
    isAfter,
    isWeekend,
    getMonth
} from 'date-fns';

import StudentInfo from '../components/dashboard/StudentInfo';
import AttendancePieChart from '../components/dashboard/AttendancePieChart';
import AttendanceTrendChart from '../components/dashboard/AttendanceTrendChart';
import AttendanceCalendar from '../components/dashboard/AttendanceCalendar';

const Dashboard: React.FC = () => {
    const [student, setStudent] = useState<Student | null>(null);
    const [attendance, setAttendance] = useState<AttendanceRecord[]>([]);
    const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
    const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
    const [selectedTrendYear, setSelectedTrendYear] = useState(new Date().getFullYear());
    const [monthlyStats, setMonthlyStats] = useState<Array<{ month: string; presentPercentage: number }>>([]);
    const [isServerDown, setIsServerDown] = useState(false);
    const { logout } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        const unsubscribe = subscribeToServerStatus(setIsServerDown);
        return () => unsubscribe();
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const studentData = await getStudentProfile();
                setStudent(studentData);
                const attendanceData = await getAttendanceRecords(
                    selectedMonth,
                    selectedYear,
                    studentData.student_id
                );
                setAttendance(attendanceData);
            } catch (error: any) {
                console.error('Error fetching data:', error);
                if (error.response?.status === 401 || error.response?.status === 403) {
                    navigate('/login');
                } else {
                    setAttendance([]);
                }
            }
        };
        fetchData();
    }, [selectedMonth, selectedYear, navigate]);

    useEffect(() => {
        const fetchMonthlyStats = async () => {
            if (student) {
                const currentMonth = selectedTrendYear === new Date().getFullYear() ? getMonth(new Date()) + 1 : 12;
                const stats = [];

                for (let month = 1; month <= currentMonth; month++) {
                    try {
                        const monthAttendance = await getAttendanceRecords(month, selectedTrendYear, student.student_id);
                        const monthEnd = new Date(selectedTrendYear, month, 0);
                        const days = Array.from(
                            { length: monthEnd.getDate() },
                            (_, i) => new Date(selectedTrendYear, month - 1, i + 1)
                        );

                        let present = 0;
                        let total = 0;

                        days.forEach(day => {
                            if (!isWeekend(day) && !isAfter(startOfDay(day), startOfDay(new Date()))) {
                                const record = monthAttendance.find(record =>
                                    isSameDay(parseISO(record.date), day)
                                );
                                if (record?.status === 'PRESENT') present++;
                                total++;
                            }
                        });

                        stats.push({
                            month: format(new Date(2000, month - 1), 'MMM'),
                            presentPercentage: total > 0 ? (present / total * 100) : 0
                        });
                    } catch (error) {
                        console.error(`Error fetching data for month ${month}:`, error);
                        stats.push({
                            month: format(new Date(2000, month - 1), 'MMM'),
                            presentPercentage: 0
                        });
                    }
                }

                setMonthlyStats(stats);
            }
        };
        fetchMonthlyStats();
    }, [selectedTrendYear, student]);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    if (!student) {
        return isServerDown ? null : <Typography>Loading...</Typography>;
    }

    const calculateAttendanceStats = () => {
        const monthEnd = new Date(selectedYear, selectedMonth, 0);
        const days = Array.from(
            { length: monthEnd.getDate() },
            (_, i) => new Date(selectedYear, selectedMonth - 1, i + 1)
        );

        let present = 0;
        let absent = 0;

        days.forEach(day => {
            if (!isWeekend(day) && !isAfter(startOfDay(day), startOfDay(new Date()))) {
                const record = attendance.find(record =>
                    isSameDay(parseISO(record.date), day)
                );
                if (record?.status === 'PRESENT') present++;
                else absent++;
            }
        });

        return { present, absent };
    };

    const { present, absent } = calculateAttendanceStats();

    return (
        <Container
            maxWidth="lg"
            sx={{
                mt: 4,
                mb: 4,
                background: 'linear-gradient(to right top, #e3f2fd, #e0f7fa)',
                borderRadius: 4,
                p: 4,
                boxShadow: '0 0 20px rgba(0,0,0,0.1)'
            }}
        >
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                <Box
                    sx={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        backgroundColor: '#ffffffcc',
                        p: 2,
                        borderRadius: 3,
                        boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
                    }}
                >
                    <Typography
                        variant="h4"
                        sx={{
                            fontWeight: 600,
                            color: '#0d47a1',
                            textShadow: '1px 1px 1px rgba(0,0,0,0.1)'
                        }}
                    >
                        Student Dashboard
                    </Typography>
                    <Button
                        variant="contained"
                        color="error"
                        sx={{
                            fontWeight: 600,
                            borderRadius: '20px',
                            px: 3,
                            py: 1,
                            boxShadow: '0 3px 8px rgba(255,0,0,0.3)',
                            transition: 'all 0.3s ease',
                            '&:hover': {
                                backgroundColor: '#b71c1c',
                                transform: 'scale(1.05)',
                            }
                        }}
                        onClick={handleLogout}
                    >
                        Logout
                    </Button>
                </Box>

                <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, gap: 3 }}>
                    <Box
                        sx={{
                            flex: 1,
                            height: '400px',
                            background: 'rgba(255,255,255,0.7)',
                            borderRadius: 3,
                            boxShadow: '0 8px 24px rgba(0,0,0,0.1)',
                            backdropFilter: 'blur(10px)',
                            p: 3,
                            display: 'flex',
                            flexDirection: 'column',
                            transition: 'transform 0.3s',
                            '&:hover': {
                                transform: 'translateY(-4px)',
                                boxShadow: '0 12px 28px rgba(0,0,0,0.15)',
                            }
                        }}
                    >
                        <StudentInfo student={student} />
                    </Box>

                    <Box
                        sx={{
                            flex: 1,
                            height: '400px',
                            background: 'rgba(255,255,255,0.7)',
                            borderRadius: 3,
                            boxShadow: '0 8px 24px rgba(0,0,0,0.1)',
                            backdropFilter: 'blur(10px)',
                            p: 3,
                            display: 'flex',
                            flexDirection: 'column',
                            transition: 'transform 0.3s',
                            '&:hover': {
                                transform: 'translateY(-4px)',
                                boxShadow: '0 12px 28px rgba(0,0,0,0.15)',
                            }
                        }}
                    >
                        <AttendancePieChart present={present} absent={absent} />
                    </Box>
                </Box>

                <Box
                    sx={{
                        background: 'rgba(255,255,255,0.9)',
                        borderRadius: 3,
                        boxShadow: '0 8px 24px rgba(0,0,0,0.08)',
                        p: 3,
                        transition: 'all 0.3s',
                        '&:hover': {
                            boxShadow: '0 12px 30px rgba(0,0,0,0.12)',
                        }
                    }}
                >
                    <AttendanceCalendar
                        attendance={attendance}
                        selectedMonth={selectedMonth}
                        selectedYear={selectedYear}
                        onMonthChange={setSelectedMonth}
                        onYearChange={setSelectedYear}
                    />
                </Box>

                <Box
                    sx={{
                        background: 'rgba(255,255,255,0.9)',
                        borderRadius: 3,
                        boxShadow: '0 8px 24px rgba(0,0,0,0.08)',
                        p: 3,
                        transition: 'all 0.3s',
                        '&:hover': {
                            boxShadow: '0 12px 30px rgba(0,0,0,0.12)',
                        }
                    }}
                >
                    <AttendanceTrendChart
                        monthlyStats={monthlyStats}
                        selectedYear={selectedTrendYear}
                        onYearChange={setSelectedTrendYear}
                    />
                </Box>
            </Box>
        </Container>
    );
};

export default Dashboard;
