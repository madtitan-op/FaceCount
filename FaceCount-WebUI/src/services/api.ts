import axios from 'axios';
import type { InternalAxiosRequestConfig } from 'axios';
import type { Student, AttendanceRecord, LoginResponse } from '../types';

const API_BASE_URL = 'http://localhost:8080';

// Create an event emitter for server status
let serverStatusListeners: ((isDown: boolean) => void)[] = [];
let isServerDown = false;

export const subscribeToServerStatus = (listener: (isDown: boolean) => void) => {
    serverStatusListeners.push(listener);
    return () => {
        serverStatusListeners = serverStatusListeners.filter(l => l !== listener);
    };
};

const updateServerStatus = (isDown: boolean) => {
    if (isServerDown !== isDown) {
        isServerDown = isDown;
        serverStatusListeners.forEach(listener => listener(isDown));
    }
};

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
        'accept': '*/*'
    }
});

// Add response interceptor to handle server status
api.interceptors.response.use(
    response => {
        updateServerStatus(false);
        return response;
    },
    error => {
        // Only mark as server down for actual connection issues
        if (error.code === 'ECONNREFUSED' || error.message === 'Network Error') {
            updateServerStatus(true);
        } else {
            // For other errors (like 401, 403, etc.), server is still up
            updateServerStatus(false);
        }
        return Promise.reject(error);
    }
);

// Add request interceptor to handle server status
api.interceptors.request.use(
    config => {
        // Exclude the login endpoint from adding the Authorization header
        if (config.url === '/api/auth/login' && config.method === 'post') {
            return config; // Do not add token for login
        }

        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        // Only mark as server down for actual connection issues
        if (error.code === 'ECONNREFUSED' || error.message === 'Network Error') {
            updateServerStatus(true);
        }
        return Promise.reject(error);
    }
);

export const login = async (userid: string, password: string): Promise<LoginResponse> => {
    try {
        console.log('Sending login request with:', { userid, password });
        const response = await api.post<string>('/api/auth/login', {
            "userid": userid,
            "password": password
        }, {
            headers: {
                'Content-Type': 'application/json',
                'accept': '*/*'
            }
        });
        console.log('Login response:', response.data);
        // Store the token
        localStorage.setItem('token', response.data);
        return { token: response.data };
    } catch (error: any) {
        console.error('Login request failed:', {
            status: error.response?.status,
            data: error.response?.data,
            config: {
                url: error.config?.url,
                method: error.config?.method,
                headers: error.config?.headers,
                data: error.config?.data
            }
        });
        throw error;
    }
};

export const getStudentProfile = async (): Promise<Student> => {
    const response = await api.get<Student>('/api/student/me');
    return response.data;
};

export const getAttendanceRecords = async (month: number, year: number, studentId: number): Promise<AttendanceRecord[]> => {
    try {
        console.log('Fetching attendance records with params:', { month, year, studentId });
        const response = await api.get<AttendanceRecord[]>(`/api/attendance/fetch/${month}/${year}`, {
            params: { userId: studentId }
        });
        console.log('Attendance records response:', response.data);
        return response.data;
    } catch (error: any) {
        console.error('Error fetching attendance records:', {
            status: error.response?.status,
            data: error.response?.data,
            config: {
                url: error.config?.url,
                method: error.config?.method,
                headers: error.config?.headers,
                params: error.config?.params
            }
        });
        throw error;
    }
}; 