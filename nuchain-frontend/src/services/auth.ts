import api from './api';
import type { User, LoginCredentials, RegisterData } from '../types/auth';

interface AuthResponse {
    user: User;
    access: string;
    refresh: string;
    message: string;
}

export const authService = {
    async login(credentials: LoginCredentials): Promise<AuthResponse> {
        const response = await api.post<AuthResponse>('/auth/login/', credentials);
        
        // Store tokens and user data
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        
        return response.data;
    },

    async register(data: RegisterData): Promise<AuthResponse> {
        const response = await api.post<AuthResponse>('/auth/register/', data);
        
        // Store tokens and user data
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        localStorage.setItem('user', JSON.stringify(response.data.user));
        
        return response.data;
    },

    async logout(): Promise<void> {
        const refreshToken = localStorage.getItem('refresh_token');
        
        try {
        await api.post('/auth/logout/', { refresh: refreshToken });
        } catch (error) {
        console.error('Logout error:', error);
        } finally {
        // Clear local storage regardless
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        }
    },

    async updateProfile(data: Partial<User>): Promise<{ user: User; message: string }> {
        const response = await api.put('/auth/profile/update/', data);
        
        // Update stored user data
        localStorage.setItem('user', JSON.stringify(response.data.user));
        
        return response.data;
    },

    async changePassword(oldPassword: string, newPassword: string): Promise<{ message: string }> {
        const response = await api.post('/auth/password/change/', {
            old_password: oldPassword,
            new_password: newPassword
        });
        
        return response.data;
    },

    async resetWallet(): Promise<{ message: string; balance: number }> {
        const response = await api.post('/auth/wallet/reset/');
        
        // Update user balance in local storage
        const user = this.getCurrentUser();
        if (user) {
        user.balance = response.data.balance;
        localStorage.setItem('user', JSON.stringify(user));
        }
        
        return response.data;
    },

    async deleteAccount(): Promise<{ message: string }> {
        const response = await api.delete('/auth/account/delete/');
        return response.data;
    },

    getCurrentUser(): User | null {
        const userStr = localStorage.getItem('user');
        return userStr ? JSON.parse(userStr) : null;
    },

    isAuthenticated(): boolean {
        return !!localStorage.getItem('access_token');
    },
};