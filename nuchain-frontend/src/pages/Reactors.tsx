import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { reactorService } from '../services/reactors';
import { investmentService } from '../services/investments';
import { ReactorList } from '../components/reactors/ReactorList';
import { InvestmentModal } from '../components/reactors/InvestmentModal';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { formatCurrency } from '../utils/helpers';
import type { Reactor } from '../types/reactor';
import './Reactors.css';

export const Reactors: React.FC = () => {
    const { user, updateUser } = useAuth();
    const [reactors, setReactors] = useState<Reactor[]>([]);
    const [selectedReactor, setSelectedReactor] = useState<Reactor | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchReactors();
    }, []);

    const fetchReactors = async () => {
        try {
            setLoading(true);
            setError('');
            const data = await reactorService.getReactors();
            setReactors(data);
        } catch (err) {
            setError('Failed to load reactors');
            console.error('Error fetching reactors:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleInvest = async (reactorId: number, amount: number) => {
        const response = await investmentService.createInvestment({
            reactor_id: reactorId,
            amount_invested: amount
        });

        // Update user balance
        if (user) {
            updateUser({
                ...user,
                balance: response.remaining_balance
            });
        }

        // Refresh reactors to update funding amounts
        await fetchReactors();

        // Show success message (you could add a toast notification here)
        alert(`Successfully invested ${amount} $NUC in ${selectedReactor?.name}!`);
    };

    return (
        <div className="reactors-page">
            <div className="page-header">
                <h1>Nuclear Reactor Marketplace</h1>
                <p className="page-subtitle">
                    Invest in the future of clean energy
                </p>
            </div>

            <div className="reactor-stats">
                <div className="stat-card">
                    <span className="stat-number">{reactors.length}</span>
                    <span className="stat-label">Available Reactors</span>
                </div>
                <div className="stat-card">
                    <span className="stat-number">{formatCurrency(user?.balance ?? 0)}</span>
                    <span className="stat-label">Wallet Balance</span>
                </div>
                <div className="stat-card">
                    <span className="stat-number">
                        {reactors.filter(r => !r.is_fully_funded).length}
                    </span>
                    <span className="stat-label">Open for Investment</span>
                </div>
            </div>

            {loading ? (
                <LoadingSpinner size="large" message="Loading reactor marketplace..." />
            ) : error ? (
                <div className="error-container">
                    <p>{error}</p>
                    <button onClick={fetchReactors} className="btn-primary">
                        Try Again
                    </button>
                </div>
            ) : (
                <ReactorList
                    reactors={reactors}
                    onInvestClick={setSelectedReactor}
                    variant="browse"
                />
            )}

            <InvestmentModal
                reactor={selectedReactor}
                isOpen={!!selectedReactor}
                onClose={() => setSelectedReactor(null)}
                onInvest={handleInvest}
            />
        </div>
    );
};