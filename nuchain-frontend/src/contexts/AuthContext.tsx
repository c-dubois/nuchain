import React, { useState, useEffect, type ReactNode } from 'react';
import type { User, RegisterData } from '../types/auth';
import { authService } from '../services/auth';
import { AuthContext } from './AuthContextBase';

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
        // Check if user is logged in on mount
        const currentUser = authService.getCurrentUser();
        if (currentUser && authService.isAuthenticated()) {
        setUser(currentUser);
        setIsAuthenticated(true);
        }
    }, []);

    const login = async (username: string, password: string) => {
        const response = await authService.login({ username, password });
        setUser(response.user);
        setIsAuthenticated(true);
    };

    const register = async (data: RegisterData) => {
        const response = await authService.register(data);
        setUser(response.user);
        setIsAuthenticated(true);
    };

    const logout = async () => {
        await authService.logout();
        setUser(null);
        setIsAuthenticated(false);
    };

    const updateUser = (updatedUser: User) => {
        setUser(updatedUser);
        localStorage.setItem('user', JSON.stringify(updatedUser));
    };

    return (
        <AuthContext.Provider
        value={{
            user,
            isAuthenticated,
            login,
            register,
            logout,
            updateUser,
        }}
        >
        {children}
        </AuthContext.Provider>
    );
};