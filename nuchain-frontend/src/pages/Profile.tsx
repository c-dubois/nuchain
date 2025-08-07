import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { authService } from '../services/auth';
import { formatCurrency } from '../utils/helpers';
import { INITIAL_BALANCE } from '../utils/constants';
import './Profile.css';

export const Profile: React.FC = () => {
    const { user, updateUser, logout } = useAuth();
    const navigate = useNavigate();
    const [isEditing, setIsEditing] = useState(false);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    
    const [formData, setFormData] = useState({
        first_name: user?.first_name || '',
        last_name: user?.last_name || '',
        email: user?.email || ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setMessage('');

        try {
            const response = await authService.updateProfile(formData);
            updateUser(response.user);
            setIsEditing(false);
            setMessage('Profile updated successfully!');
        } catch {
            setError('Failed to update profile. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleResetWallet = async () => {
        if (!window.confirm(
            'Are you sure you want to reset your wallet? This will:\n' +
            '• Set your balance back to 25,000 $NUC\n' +
            '• Clear all your investments\n' +
            '• Remove funding from reactors\n\n' +
            'This action cannot be undone!'
        )) {
            return;
        }

        setLoading(true);
        setError('');
        setMessage('');

        try {
            const response = await authService.resetWallet();
            if (user) {
                updateUser({
                    ...user,
                    balance: response.balance
                });
            }
            setMessage('Wallet reset successfully! Your balance is now 25,000 $NUC.');
        } catch {
            setError('Failed to reset wallet. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = async () => {
        if (window.confirm('Are you sure you want to logout?')) {
            await logout();
            navigate('/');
        }
    };

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <div className="profile-page">
            <h1>User Profile</h1>

            {message && <div className="success-message">{message}</div>}
            {error && <div className="error-message">{error}</div>}

            <div className="profile-grid">
                <div className="profile-section">
                    <h2>Account Information</h2>
            
                    {!isEditing ? (
                        <div className="profile-info">
                            <div className="info-row">
                                <span className="info-label">Username:</span>
                                <span className="info-value">{user.username}</span>
                            </div>
                            <div className="info-row">
                                <span className="info-label">Name:</span>
                                <span className="info-value">
                                    {user.first_name || user.last_name 
                                        ? `${user.first_name} ${user.last_name}`.trim()
                                        : 'Not set'}
                                </span>
                            </div>
                            <div className="info-row">
                                <span className="info-label">Email:</span>
                                <span className="info-value">{user.email}</span>
                            </div>
                
                            <button 
                                className="btn-secondary"
                                onClick={() => setIsEditing(true)}
                            >
                                Edit Profile
                            </button>
                        </div>
                    ) : (
                        <form onSubmit={handleSubmit} className="profile-form">
                            <div className="form-group">
                                <label htmlFor="first_name">First Name</label>
                                <input
                                    id="first_name"
                                    name="first_name"
                                    type="text"
                                    value={formData.first_name}
                                    onChange={handleChange}
                                    placeholder="John"
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
                                    placeholder="Doe"
                                />
                            </div>
                
                            <div className="form-group">
                                <label htmlFor="email">Email</label>
                                <input
                                    id="email"
                                    name="email"
                                    type="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    required
                                />
                            </div>
                
                            <div className="form-buttons">
                                <button 
                                    type="button"
                                    className="btn-secondary"
                                    onClick={() => {
                                        setIsEditing(false);
                                        setFormData({
                                            first_name: user.first_name || '',
                                            last_name: user.last_name || '',
                                            email: user.email || ''
                                        });
                                    }}
                                    disabled={loading}
                                >
                                    Cancel
                                </button>
                                <button 
                                    type="submit"
                                    className="btn-primary"
                                    disabled={loading}
                                >
                                    {loading ? 'Saving...' : 'Save Changes'}
                                </button>
                            </div>
                        </form>
                    )}
                </div>

                <div className="profile-section">
                    <h2>Wallet Information</h2>
                    
                    <div className="wallet-info">
                        <div className="balance-display">
                            <span className="balance-label">Current Balance</span>
                            <span className="balance-value">{formatCurrency(user.balance)}</span>
                        </div>
                    
                        <div className="wallet-actions">
                            <p className="wallet-description">
                                Reset your wallet to start fresh with {formatCurrency(INITIAL_BALANCE)}.<br />
                                This will clear all investments and return funding to reactors.
                            </p>
                        
                            <button 
                                className="btn-secondary"
                                onClick={handleResetWallet}
                                disabled={loading}
                            >
                                {loading ? 'Resetting...' : '🔄 Reset Wallet'}
                            </button>
                        </div>
                    </div>
                </div>

                <div className="profile-section">
                    <h2>Account Actions</h2>

                    <div className="account-actions">
                        <div className="action-item">
                            <h3>🚪 Logout</h3>
                            <p>Sign out of your NuChain account</p>
                            <button 
                                className="btn-secondary"
                                onClick={handleLogout}
                            >
                                Logout
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};