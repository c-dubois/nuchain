import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import './Header.css';

export const Header: React.FC = () => {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        await logout();
        navigate('/');
    };

    const closeSidebar = () => {
        setSidebarOpen(false);
    };

    return (
        <>
        <header className="header">
            <div className="header-content">
            <button 
                className="menu-button"
                onClick={() => setSidebarOpen(!sidebarOpen)}
                aria-label="Toggle menu"
            >
                <span className="hamburger-line"></span>
                <span className="hamburger-line"></span>
                <span className="hamburger-line"></span>
            </button>

            <Link to="/dashboard" className="logo-link">
                <h1 className="logo">⚛️ NuChain</h1>
            </Link>

            <div className="balance-display">
                <span className="balance-label">Balance:</span>
                <span className="balance-amount">{user?.balance.toLocaleString()} $NUC</span>
            </div>
            </div>
        </header>

        {/* Sidebar */}
        <div className={`sidebar-overlay ${sidebarOpen ? 'open' : ''}`} onClick={closeSidebar}></div>
        <nav className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
            <div className="sidebar-header">
            <h2>Menu</h2>
            <button className="close-button" onClick={closeSidebar}>×</button>
            </div>
            
            <ul className="sidebar-menu">
            <li>
                <Link to="/dashboard" onClick={closeSidebar}>
                📊 Portfolio Dashboard
                </Link>
            </li>
            <li>
                <Link to="/invest" onClick={closeSidebar}>
                💰 Invest Now
                </Link>
            </li>
            <li>
                <Link to="/profile" onClick={closeSidebar}>
                👤 Profile
                </Link>
            </li>
            <li>
                <button onClick={handleLogout} className="logout-button">
                🚪 Logout
                </button>
            </li>
            </ul>
        </nav>
        </>
    );
};