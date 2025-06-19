import React from 'react';
import { Paper, Typography, Box, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameDay, parseISO, isAfter, startOfDay, isWeekend } from 'date-fns';
import type { AttendanceRecord } from '../../types';

interface AttendanceCalendarProps {
    attendance: AttendanceRecord[];
    selectedMonth: number;
    selectedYear: number;
    onMonthChange: (month: number) => void;
    onYearChange: (year: number) => void;
}

const AttendanceCalendar: React.FC<AttendanceCalendarProps> = ({
    attendance,
    selectedMonth,
    selectedYear,
    onMonthChange,
    onYearChange
}) => {
    const getAttendanceStatus = (date: Date) => {
        if (isAfter(startOfDay(date), startOfDay(new Date())) || isWeekend(date)) {
            return null;
        }
        
        const record = attendance.find(record => 
            isSameDay(parseISO(record.date), date)
        );
        return record?.status || 'ABSENT';
    };

    const renderCalendar = () => {
        const monthStart = startOfMonth(new Date(selectedYear, selectedMonth - 1));
        const monthEnd = endOfMonth(monthStart);
        const days = eachDayOfInterval({ start: monthStart, end: monthEnd });
        
        const startDay = monthStart.getDay();
        const paddingDays = Array(startDay).fill(null);

        return (
            <Box sx={{ width: '100%', overflowX: 'auto' }}>
                <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gap: 1, minWidth: 500 }}>
                    {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
                        <Box key={day} sx={{ p: 1, textAlign: 'center', fontWeight: 'bold' }}>
                            {day}
                        </Box>
                    ))}
                    
                    {paddingDays.map((_, index) => (
                        <Box
                            key={`padding-${index}`}
                            sx={{
                                p: 1,
                                textAlign: 'center',
                                border: '1px solid #ddd',
                                borderRadius: 1,
                                bgcolor: 'grey.100',
                                minHeight: '40px'
                            }}
                        />
                    ))}
                    
                    {days.map((day, index) => {
                        const status = getAttendanceStatus(day);
                        const isFutureOrWeekend = status === null;
                        const isWeekendDay = isWeekend(day);
                        
                        return (
                            <Box
                                key={index}
                                sx={{
                                    p: 1,
                                    textAlign: 'center',
                                    border: '1px solid #ddd',
                                    borderRadius: 1,
                                    bgcolor: isFutureOrWeekend ? 'grey.300' : (status === 'PRESENT' ? 'success.light' : 'error.light'),
                                    color: isFutureOrWeekend ? 'grey.600' : 'white',
                                    minHeight: '40px',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    justifyContent: 'center'
                                }}
                            >
                                <Typography variant="body2">
                                    {format(day, 'd')}
                                </Typography>
                                {!isFutureOrWeekend && (
                                    <Typography variant="caption">
                                        {status}
                                    </Typography>
                                )}
                                {isWeekendDay && (
                                    <Typography variant="caption">
                                        Weekend
                                    </Typography>
                                )}
                            </Box>
                        );
                    })}
                </Box>
            </Box>
        );
    };

    return (
        <Paper sx={{ p: 2 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">Attendance Records</Typography>
                <Box>
                    <FormControl sx={{ minWidth: 120, mr: 2 }}>
                        <InputLabel>Month</InputLabel>
                        <Select
                            value={selectedMonth}
                            label="Month"
                            onChange={(e) => onMonthChange(Number(e.target.value))}
                        >
                            {Array.from({ length: 12 }, (_, i) => (
                                <MenuItem key={i + 1} value={i + 1}>
                                    {format(new Date(2000, i), 'MMMM')}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <FormControl sx={{ minWidth: 120 }}>
                        <InputLabel>Year</InputLabel>
                        <Select
                            value={selectedYear}
                            label="Year"
                            onChange={(e) => onYearChange(Number(e.target.value))}
                        >
                            {Array.from({ length: 5 }, (_, i) => {
                                const year = new Date().getFullYear() - 2 + i;
                                return (
                                    <MenuItem key={year} value={year}>
                                        {year}
                                    </MenuItem>
                                );
                            })}
                        </Select>
                    </FormControl>
                </Box>
            </Box>
            {renderCalendar()}
        </Paper>
    );
};

export default AttendanceCalendar; 