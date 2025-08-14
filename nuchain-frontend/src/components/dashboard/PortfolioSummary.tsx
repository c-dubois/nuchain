import React from 'react';
import { Link } from 'react-router-dom';
import { TimeButtonGroup } from './TimeButtonGroup';
import type { PortfolioSummary as PortfolioSummaryType } from '../../types/investment';
import type { TimePeriod } from '../../utils/constants';
import { formatCurrency, formatPercentage, formatCarbonOffset } from '../../utils/helpers';
import './PortfolioSummary.css';

interface PortfolioSummaryProps {
    summary: PortfolioSummaryType | null;
    selectedPeriod: TimePeriod;
    onPeriodChange: (period: TimePeriod) => void;
    loading?: boolean;
}

export const PortfolioSummary: React.FC<PortfolioSummaryProps> = ({
    summary,
    selectedPeriod,
    onPeriodChange,
    loading = false
}) => {
    if (loading) {
        return (
            <div className="portfolio-summary loading">
                <div className="summary-skeleton"></div>
            </div>
        );
    }

    if (!summary || summary.investment_count === 0) {
        return (
            <div className="portfolio-summary empty">
                <h2>Portfolio Summary</h2>
                <div className="empty-state">
                    <p>🚀 No investments yet!</p>
                    <p>Start investing in nuclear reactors to see your portfolio grow!</p>
                    <Link to="/invest" className="btn-browse-reactors">
                        Browse Reactors
                    </Link>
                </div>
            </div>
        );
    }

    const currentProjection = summary.projections.find(
        (p) => p.time_period_years === selectedPeriod
    ) || summary.projections[0];

    return (
        <div className="portfolio-summary">
            <h2>Portfolio Summary</h2>

            <div className="summary-grid">
                <div className="summary-card">
                    <div className="card-header">
                        <span className="card-icon">💰</span>
                        <h3>Total Invested</h3>
                    </div>
                    <p className="card-value">{formatCurrency(summary.total_invested)}</p>
                    <p className="card-subtitle">
                        Across {summary.investment_count} {summary.investment_count === 1 ? 'investment' : 'investments'}
                    </p>
                </div>

                <div className="summary-card">
                    <div className="card-header">
                        <span className="card-icon">📈</span>
                        <h3>Projected Return ({selectedPeriod}y)</h3>
                    </div>
                    <p className="card-value">{formatCurrency(currentProjection.total_return)}</p>
                    <p className={`card-subtitle ${currentProjection.roi_percentage >= 0 ? 'positive' : 'negative'}`}>
                        {currentProjection.roi_percentage >= 0 ? '+' : ''}{formatPercentage(currentProjection.roi_percentage)} ROI
                    </p>
                </div>

                <div className="summary-card">
                    <div className="card-header">
                        <span className="card-icon">🌱</span>
                        <h3>Carbon Offset ({selectedPeriod}y)</h3>
                    </div>
                    <p className="card-value">{formatCarbonOffset(currentProjection.total_carbon_offset)}</p>
                    <p className="card-subtitle">Environmental impact</p>
                </div>
                
            <TimeButtonGroup
                selectedPeriod={selectedPeriod}
                onPeriodChange={onPeriodChange}
            />
            </div>
        </div>
    );
};