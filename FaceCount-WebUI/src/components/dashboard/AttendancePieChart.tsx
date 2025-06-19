import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

interface AttendancePieChartProps {
    present: number;
    absent: number;
}

const AttendancePieChart: React.FC<AttendancePieChartProps> = ({ present, absent }) => {
    const data = [
        { 
            name: 'Present', 
            value: present, 
            color: '#4caf50',
            percentage: present + absent > 0 ? (present / (present + absent) * 100).toFixed(1) : '0.0'
        },
        { 
            name: 'Absent', 
            value: absent, 
            color: '#f44336',
            percentage: present + absent > 0 ? (absent / (present + absent) * 100).toFixed(1) : '0.0'
        }
    ];

    return (
        <Card>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    Attendance Statistics
                </Typography>
                <Box sx={{ height: 300 }}>
                    <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                            <Pie
                                data={data}
                                dataKey="value"
                                nameKey="name"
                                cx="50%"
                                cy="50%"
                                outerRadius={80}
                                // label={({ name, value, percentage }) => 
                                //     `${name}: ${value} days (${percentage}%)`
                                // }
                            >
                                {data.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.color} />
                                ))}
                            </Pie>
                            <Tooltip 
                                formatter={(value, name, props) => [
                                    `${value} days (${props.payload.percentage}%)`,
                                    name
                                ]}
                            />
                            <Legend />
                        </PieChart>
                    </ResponsiveContainer>
                </Box>
            </CardContent>
        </Card>
    );
};

export default AttendancePieChart; 