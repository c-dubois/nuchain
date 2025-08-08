import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import type { RegisterData } from '../../types/auth';
import { AxiosError } from 'axios';
import './AuthForms.css';

interface RegisterFormProps {
    onSuccess: () => void;
    onSwitchToLogin: () => void;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({ onSuccess, onSwitchToLogin }) => {
    const [formData, setFormData] = useState<RegisterData>({
        username: '',
        email: '',
        password: '',
        password_confirm: '',
        first_name: '',
        last_name: '',
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { register } = useAuth();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
        ...formData,
        [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        
        if (formData.password !== formData.password_confirm) {
        setError('Passwords do not match');
        return;
        }
        
        setLoading(true);

        try {
            await register(formData);
            onSuccess();
        } catch (err) {
            if (err instanceof AxiosError) {
                setError(err.response?.data?.email?.[0] || 
                    err.response?.data?.username?.[0] || 
                    err.response?.data?.password?.[0] || 'Registration failed. Please try again.');
            } else {
                setError('An unexpected error occurred. Please try again.');
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <form className="auth-form" onSubmit={handleSubmit}>
        <h2 className="auth-title">Create Account</h2>
        <p className="auth-subtitle">Start with 25,000 $NUC tokens!</p>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-row">
            <div className="form-group">
            <label htmlFor="first_name">First Name</label>
            <input
                id="first_name"
                name="first_name"
                type="text"
                value={formData.first_name}
                onChange={handleChange}
                placeholder="Fusion"
            />
            </div>

            <div className="form-group">
            <label htmlFor="last_name">Last Name</label>
            <input
                id="last_name"
                name="last_name"
                type="text"
                value={formData.last_name}
                onChange={handleChange}
                placeholder="Fanatic"
            />
            </div>
        </div>

        <div className="form-group">
            <label htmlFor="username">Username*</label>
            <input
            id="username"
            name="username"
            type="text"
            value={formData.username}
            onChange={handleChange}
            required
            placeholder="the_future_is_nuclear"
            />
        </div>

        <div className="form-group">
            <label htmlFor="email">Email*</label>
            <input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            required
            placeholder="fusion_fanatic@nuchain.com"
            />
        </div>

        <div className="form-group">
            <label htmlFor="password">Password*</label>
            <input
            id="password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            required
            placeholder="Min 8 characters"
            minLength={8}
            />
        </div>

        <div className="form-group">
            <label htmlFor="password_confirm">Confirm Password*</label>
            <input
            id="password_confirm"
            name="password_confirm"
            type="password"
            value={formData.password_confirm}
            onChange={handleChange}
            required
            placeholder="Re-enter password"
            />
        </div>

        <button 
            type="submit" 
            className="btn-primary auth-button"
            disabled={loading}
        >
            {loading ? 'Creating Account...' : 'Sign Up'}
        </button>

        <p className="auth-switch">
            Already have an account?{' '}
            <button 
            type="button"
            onClick={onSwitchToLogin}
            className="link-button"
            >
            Login
            </button>
        </p>
        </form>
    );
};