export interface Student {
    student_id: number;
    name: string;
    yop: number;
    department: string;
    email: string;
    role: string;
}

export interface AttendanceRecord {
    name: string;
    userId: number;
    status: 'PRESENT' | 'ABSENT';
    date: string;
    time: string;
    marked_by_faculty_id: number;
    marked_by_system_id: number | null;
}

export interface LoginResponse {
    token: string;
}

export interface AuthState {
    token: string | null;
    isAuthenticated: boolean;
} 