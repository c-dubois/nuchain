import React from 'react';
import './LoadingSpinner.css';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  message?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ 
    size = 'medium', 
    message 
}) => {
    return (
        <div className="loading-container">
            <div className={`loading-spinner loading-spinner-${size}`}></div>
            {message && <p className="loading-message">{message}</p>}
        </div>
    );
};