import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { authService } from '../services/auth';
import { formatCurrency } from '../utils/helpers';
import { INITIAL_BALANCE } from '../utils/constants';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import './Profile.css';

export const Profile: React.FC = () => {
    const { user, updateUser, logout } = useAuth();
    const navigate = useNavigate();
    
    const [isEditing, setIsEditing] = useState(false);
    const [loading, setLoading] = useState(false);
    
    const [passwordLoading, setPasswordLoading] = useState(false);
    const [deleteLoading, setDeleteLoading] = useState(false);
    
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    
    const [formData, setFormData] = useState({
        first_name: user?.first_name || '',
        last_name: user?.last_name || '',
        email: user?.email || ''
    });
    
    const [passwords, setPasswords] = useState({
        oldPassword: '',
        newPassword: '',
        confirmNewPassword: ''
    });
    
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };
    
    const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPasswords({
            ...passwords,
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
            window.scrollTo(0, 0);
        } catch {
            setError('Failed to update profile. Please try again.');
            window.scrollTo(0, 0);
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
            window.scrollTo(0, 0);
        } catch {
            setError('Failed to reset wallet. Please try again.');
            window.scrollTo(0, 0);
        } finally {
            setLoading(false);
        }
    };
    
    const handleChangePassword = async (e: React.FormEvent) => {
        e.preventDefault();
        
        setError('');
        setMessage('');
        
        if (passwords.newPassword !== passwords.confirmNewPassword) {
            setError("New password and confirmation do not match.");
            window.scrollTo(0, 0);
            return;
        }
        
        setPasswordLoading(true);
        
        try {
            await authService.changePassword(passwords.oldPassword, passwords.newPassword);
            setMessage('Password changed successfully!');
            setPasswords({ oldPassword: '', newPassword: '', confirmNewPassword: '' });
            window.scrollTo(0, 0);
        } catch {
            setError('Failed to change password');
            window.scrollTo(0, 0);
        } finally {
            setPasswordLoading(false);
        }
    };
    
    const handleDeleteAccount = async () => {
        if (
            !window.confirm(
                'Are you sure? This will permanently delete your account and all investments.'
            )
        ) {
            return;
        }
        
        setDeleteLoading(true);
        setError('');
        setMessage('');
        
        try {
            await authService.deleteAccount();
            await logout();
            navigate('/');
        } catch {
            setError('Failed to delete account. Please try again later.');
        } finally {
            setDeleteLoading(false);
        }
    };
    
    const handleLogout = async () => {
        if (window.confirm('Are you sure you want to logout?')) {
            await logout();
            navigate('/');
        }
    };
    
    if (!user) {
        return <LoadingSpinner />;
    }
    
    return (
        <div className="profile-page">
            <h1>{user.first_name}'s Profile</h1>
            
            {message && <div className="success-message-profile">{message}</div>}
            {error && <div className="error-message-profile">{error}</div>}
            
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
                                    className="btn-primary"
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
                                    className="btn-secondary"
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
                        <div className="profile-balance-display">
                            <span className="profile-balance-label">Current Balance</span>
                            <span className="profile-balance-value">{formatCurrency(user.balance)}</span>
                        </div>
                        
                        {user.wallet && (
                            <div className="wallet-address-display">
                                <span className="info-label">Wallet Address:</span>
                                <code className="wallet-address">{user.wallet.address}</code>
                                <a 
                                    href={user.wallet.basescan_url} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="basescan-link"
                                >
                                    View on BaseScan ↗
                                </a>
                            </div>
                        )}
                        
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
                    <h2>Change Password</h2>
                    <form onSubmit={handleChangePassword} className="profile-form">
                        <div className="form-group">
                            <label htmlFor="oldPassword">Current Password</label>
                            <input
                                id="oldPassword"
                                name="oldPassword"
                                type="password"
                                value={passwords.oldPassword}
                                onChange={handlePasswordChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="newPassword">New Password</label>
                            <input
                                id="newPassword"
                                name="newPassword"
                                type="password"
                                value={passwords.newPassword}
                                onChange={handlePasswordChange}
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label htmlFor="confirmNewPassword">Confirm New Password</label>
                            <input
                                id="confirmNewPassword"
                                name="confirmNewPassword"
                                type="password"
                                value={passwords.confirmNewPassword}
                                onChange={handlePasswordChange}
                                required
                            />
                        </div>
                        <button type="submit" className="btn-secondary" disabled={passwordLoading}>
                            {passwordLoading ? 'Changing...' : 'Change Password'}
                        </button>
                    </form>
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
                        
                        <div className="action-item">
                            <h3>🗑️ Delete Account</h3>
                            <p>Warning: This action is irreversible and will delete all of your data</p>
                            <button className="btn-danger" onClick={handleDeleteAccount} disabled={deleteLoading}>
                                {deleteLoading ? 'Deleting...' : 'Delete Account'}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};