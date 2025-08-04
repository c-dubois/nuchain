import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import './AuthForms.css';

interface LoginFormProps {
    onSuccess: () => void;
    onSwitchToRegister: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSuccess, onSwitchToRegister }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
        await login(username, password);
        onSuccess();
        } catch (err: any) {
        setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
        } finally {
        setLoading(false);
        }
    };

    return (
        <form className="auth-form" onSubmit={handleSubmit}>
        <h2 className="auth-title">Welcome Back</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            placeholder="Enter your username"
            />
        </div>

        <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="Enter your password"
            />
        </div>

        <button 
            type="submit" 
            className="btn-primary auth-button"
            disabled={loading}
        >
            {loading ? 'Logging in...' : 'Login'}
        </button>

        <p className="auth-switch">
            Don't have an account?{' '}
            <button 
            type="button"
            onClick={onSwitchToRegister}
            className="link-button"
            >
            Sign up
            </button>
        </p>
        </form>
    );
};