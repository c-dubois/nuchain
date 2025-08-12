import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { investmentService, reactorService } from '../services/investments';
import { PortfolioSummary } from '../components/dashboard/PortfolioSummary';
import { InvestmentChart } from '../components/dashboard/InvestmentChart';
import { ReactorList } from '../components/reactors/ReactorList';
import { InvestmentModal } from '../components/reactors/InvestmentModal';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import type { PortfolioSummary as PortfolioSummaryType } from '../types/investment';
import type { Investment } from '../types/investment';
import type { Reactor } from '../types/reactor';
import type { TimePeriod } from '../utils/constants';
import './Dashboard.css';

export const Dashboard: React.FC = () => {
    const { user, updateUser } = useAuth();
    const [portfolioSummary, setPortfolioSummary] = useState<PortfolioSummaryType | null>(null);
    const [investments, setInvestments] = useState<Investment[]>([]);
    const [reactors, setReactors] = useState<Reactor[]>([]);
    const [selectedPeriod, setSelectedPeriod] = useState<TimePeriod>(1);
    const [selectedReactor, setSelectedReactor] = useState<Reactor | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        try {
            setLoading(true);
            setError('');

            const [summaryData, investmentsData, reactorsData] = await Promise.all([
                investmentService.getPortfolioSummary(),
                investmentService.getInvestments(),
                reactorService.getReactors()
            ]);

            setPortfolioSummary(summaryData);
            setInvestments(investmentsData);
            setReactors(reactorsData);
        } catch (err) {
            setError('Failed to load dashboard data');
            console.error('Dashboard error:', err);
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

        // Refresh dashboard data
        await fetchDashboardData();
    };

    if (loading) {
        return <LoadingSpinner size="large" message="Loading your portfolio..." />;
    }

    if (error) {
        return (
            <div className="dashboard-error">
                <h2>Error</h2>
                <p>{error}</p>
                <button onClick={fetchDashboardData} className="btn-primary">
                    Try Again
                </button>
            </div>
        );
    }

    // Get invested reactors
    const investedReactors = reactors.filter(reactor =>
        investments.some(inv => inv.reactor.id === reactor.id)
    );

    // Create investment amounts map
    const investmentAmounts = investments.reduce((acc, inv) => {
        acc[inv.reactor.id] = inv.amount_invested;
        return acc;
    }, {} as Record<number, number>);

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <h1>Your Nuclear Energy Investment Portfolio</h1>
                <p className="dashboard-subtitle">
                    Track your investments and environmental impact!
                </p>
            </div>

            <div className="dashboard-grid">
                <div className="dashboard-main">
                    <PortfolioSummary
                        summary={portfolioSummary}
                        selectedPeriod={selectedPeriod}
                        onPeriodChange={setSelectedPeriod}
                        loading={loading}
                    />

                    {investedReactors.length > 0 ? (
                        <div className="portfolio-reactors">
                            <h3>Your Reactor Investments</h3>
                            <ReactorList
                                reactors={investedReactors}
                                onInvestClick={setSelectedReactor}
                                variant="portfolio"
                                investments={investmentAmounts}
                                portfolioTotal={portfolioSummary?.total_invested || 0}
                            />
                        </div>
                        ) : (
                            <div className="no-investments">
                            <p>No investments yet!</p>
                            <Link to="/invest" className="btn-browse-reactors">
                                Browse Reactors
                            </Link>
                        </div>
                        )}
                        </div>

                <div className="dashboard-sidebar">
                    {portfolioSummary && portfolioSummary.investment_count > 0 && (
                        <InvestmentChart 
                            summary={portfolioSummary} 
                            investments={investments}
                        />
                    )}
                </div>
            </div>

            <InvestmentModal
                reactor={selectedReactor}
                isOpen={!!selectedReactor}
                onClose={() => setSelectedReactor(null)}
                onInvest={handleInvest}
            />
        </div>
    );
};