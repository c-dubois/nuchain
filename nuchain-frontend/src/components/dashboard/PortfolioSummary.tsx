import React from 'react';
import type { PortfolioSummary as PortfolioSummaryType } from '../../types/investment';
import type { TimePeriod } from '../../utils/constants';
import { formatCurrency, formatPercentage, formatCarbonOffset } from '../../utils/helpers';
import './PortfolioSummary.css';

interface PortfolioSummaryProps {
    summary: PortfolioSummaryType | null;
    selectedPeriod: TimePeriod;
    loading?: boolean;
}

export const PortfolioSummary: React.FC<PortfolioSummaryProps> = ({
    summary,
    selectedPeriod,
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
                    <p className="card-subtitle">Across {summary.investment_count} investments</p>
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
            </div>

            <div className="portfolio-details">
                <h4>Investment Breakdown</h4>
                <div className="reactor-list">
                    {summary.reactors_invested_in.map((reactor, index) => (
                        <div key={index} className="reactor-item">
                            <span className="reactor-icon">⚛️</span>
                            <span>{reactor}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};