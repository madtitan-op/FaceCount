import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import type { Student } from '../../types';

interface StudentInfoProps {
    student: Student;
}

const StudentInfo: React.FC<StudentInfoProps> = ({ student }) => {
    return (
        <Card>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    Student Information
                </Typography>
                <Typography><strong>Name:</strong> {student.name}</Typography>
                <Typography><strong>Roll No:</strong> {student.student_id}</Typography>
                <Typography><strong>Department:</strong> {student.department}</Typography>
                <Typography><strong>Year of Passing:</strong> {student.yop}</Typography>
                <Typography><strong>E-mail:</strong> {student.email}</Typography>
            </CardContent>
        </Card>
    );
};

export default StudentInfo; 