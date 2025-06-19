import React, { createContext, useContext, useState, useEffect } from 'react';
import type { AuthState } from '../types';
import { login as apiLogin } from '../services/api';

interface AuthContextType extends AuthState {
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [authState, setAuthState] = useState<AuthState>({
        token: localStorage.getItem('token'),
        isAuthenticated: !!localStorage.getItem('token'),
    });

    const login = async (email: string, password: string) => {
        try {
            const response = await apiLogin(email, password);
            localStorage.setItem('token', response.token);
            setAuthState({
                token: response.token,
                isAuthenticated: true,
            });
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        setAuthState({
            token: null,
            isAuthenticated: false,
        });
    };

    return (
        <AuthContext.Provider value={{ ...authState, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}; 