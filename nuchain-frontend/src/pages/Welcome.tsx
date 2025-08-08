import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LoginForm } from '../components/auth/LoginForm';
import { RegisterForm } from '../components/auth/RegisterForm';
import './Welcome.css';

export const Welcome: React.FC = () => {
    const [showRegister, setShowRegister] = useState(false);
    const navigate = useNavigate();

    const handleAuthSuccess = () => {
        navigate('/dashboard');
    };

    const handleSwitchToRegister = () => {
        setShowRegister(true);
    };

    const handleSwitchToLogin = () => {
        setShowRegister(false);
    };

    return (
        <div className="welcome-container">
            <div className="welcome-content">
                <div className="welcome-hero">
                    <h1 className="welcome-title">
                        <span className="nuclear-symbol">⚛️</span> NuChain
                    </h1>
                    <p className="welcome-tagline">
                        The Future of Nuclear Investment
                    </p>
                    <div className="welcome-description">
                        <p>
                        Invest in fictional nuclear reactors with mock $NUC tokens.<br />
                        Track your ROI and carbon offset impact while learning about
                        clean energy infrastructure.
                        </p>
                    </div>
                
                    <div className="features-grid">
                        <div className="feature-card">
                            <span className="feature-icon">💰</span>
                            <h3>25,000 $NUC</h3>
                            <p>Starting balance for every user</p>
                        </div>
                        <div className="feature-card">
                            <span className="feature-icon">⚡</span>
                            <h3>6 Reactors</h3>
                            <p>Unique investment opportunities</p>
                        </div>
                        <div className="feature-card">
                            <span className="feature-icon">🌱</span>
                            <h3>Track Impact</h3>
                            <p>Monitor ROI & carbon offset</p>
                        </div>
                    </div>
                </div>

                <div className="auth-section">
                    {showRegister ? (
                        <RegisterForm
                            key="register"
                            onSuccess={handleAuthSuccess}
                            onSwitchToLogin={handleSwitchToLogin}
                        />
                    ) : (
                        <LoginForm
                            key="login"
                            onSuccess={handleAuthSuccess}
                            onSwitchToRegister={handleSwitchToRegister}
                        />
                    )}
                </div>
            </div>
        </div>
    );
};