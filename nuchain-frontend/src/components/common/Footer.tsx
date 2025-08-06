import React from 'react';
import './Footer.css';

export const Footer: React.FC = () => {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="footer">
            <div className="footer-content">
                <p className="footer-text">
                    ⚛️ NuChain | Fueling tomorrow.
                </p>
                <p className="footer-disclaimer">
                    This is a simulation platform. No real investments or transactions occur.
                </p>
                <p className="footer-copyright">
                    © {currentYear} Camille DuBois. All rights reserved.
                </p>
            </div>
        </footer>
    );
};