import React from 'react';
import type { Reactor } from '../../types/reactor';
import { ReactorCard } from './ReactorCard';
import { LoadingSpinner } from '../common/LoadingSpinner';
import './ReactorList.css';

interface ReactorListProps {
    reactors: Reactor[];
    loading?: boolean;
    error?: string;
    onInvestClick: (reactor: Reactor) => void;
    variant?: 'browse' | 'portfolio';
    investments?: Record<number, number>;
    portfolioTotal?: number;
}

export const ReactorList: React.FC<ReactorListProps> = ({
    reactors,
    loading = false,
    error,
    onInvestClick,
    variant = 'browse',
    investments = {},
    portfolioTotal
}) => {
    if (loading) {
        return <LoadingSpinner message="Loading reactors..." />;
    }

    if (error) {
        return (
            <div className="reactor-list-error">
                <p>❌ Error loading reactors: {error}</p>
            </div>
        );
    }

    if (reactors.length === 0) {
        return (
            <div className="reactor-list-empty">
                <p>🔍 No reactors available at the moment.</p>
            </div>
        );
    }

    return (
        <div className={`reactor-list reactor-list-${variant}`}>
            {reactors.map((reactor) => (
                <ReactorCard
                    key={reactor.id}
                    reactor={reactor}
                    onInvestClick={onInvestClick}
                    variant={variant}
                    investmentAmount={investments[reactor.id]}
                    portfolioTotal={portfolioTotal}
                />
            ))}
        </div>
    );
};