import React from 'react';
import { Card, CardContent, Typography, Box, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface MonthlyStat {
    month: string;
    presentPercentage: number;
}

interface AttendanceTrendChartProps {
    monthlyStats: MonthlyStat[];
    selectedYear: number;
    onYearChange: (year: number) => void;
}

const AttendanceTrendChart: React.FC<AttendanceTrendChartProps> = ({ 
    monthlyStats, 
    selectedYear, 
    onYearChange 
}) => {
    return (
        <Card>
            <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h6">
                        Monthly Attendance Trend
                    </Typography>
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
                <Box sx={{ height: 300 }}>
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart
                            data={monthlyStats}
                            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                        >
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="month" />
                            <YAxis 
                                domain={[0, 100]}
                                label={{ 
                                    value: 'Attendance %', 
                                    angle: -90, 
                                    position: 'insideLeft',
                                    style: { textAnchor: 'middle' }
                                }}
                            />
                            <Tooltip 
                                formatter={(value: number) => [`${value.toFixed(1)}%`, 'Attendance']}
                            />
                            <Line
                                type="monotone"
                                dataKey="presentPercentage"
                                stroke="#4caf50"
                                strokeWidth={2}
                                dot={{ r: 4 }}
                                activeDot={{ r: 6 }}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </Box>
            </CardContent>
        </Card>
    );
};

export default AttendanceTrendChart; 