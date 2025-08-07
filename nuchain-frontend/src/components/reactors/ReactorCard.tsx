import React from 'react';
import type { Reactor } from '../../types/reactor';
import { formatCurrency, formatROIRate, formatCarbonOffset, getReactorImage } from '../../utils/helpers';
import './ReactorCard.css';

interface ReactorCardProps {
    reactor: Reactor;
    onInvestClick: (reactor: Reactor) => void;
    variant?: 'browse' | 'portfolio';
    investmentAmount?: number;
}

export const ReactorCard: React.FC<ReactorCardProps> = ({ 
    reactor, 
    onInvestClick,
    variant = 'browse',
    investmentAmount 
}) => {
    const fundingPercentage = reactor.funding_percentage || 0;
    const isFullyFunded = reactor.is_fully_funded;

    return (
        <div className={`reactor-card ${variant}`}>
            <div className="reactor-image-container">
                <img 
                    src={getReactorImage(reactor.slug)} 
                    alt={reactor.name}
                    className="reactor-image"
                    onError={(e) => {
                        (e.target as HTMLImageElement).src = 'https://via.placeholder.com/400x250/2a2829/daff02?text=' + reactor.name;
                    }}
                />
                <div className="reactor-type-badge">{reactor.type}</div>
            </div>

            <div className="reactor-content">
                <h3 className="reactor-name">{reactor.name}</h3>
                <p className="reactor-location">📍 {reactor.location}</p>

                <div className="reactor-stats">
                    <div className="stat">
                        <span className="stat-label">Return on Investment (ROI)</span>
                        <span className={`stat-value ${reactor.annual_roi_rate < 0 ? 'negative' : 'positive'}`}>{formatROIRate(reactor.annual_roi_rate)}</span>
                    </div>
                    <div className="stat">
                        <span className="stat-label">Carbon Offset</span>
                        <span className="stat-value">{formatCarbonOffset(reactor.carbon_offset_tonnes_co2_per_nuc_per_year)}</span>
                    </div>
                </div>

                {variant === 'browse' && (
                    <>
                        <p className="reactor-description">{reactor.description}</p>

                        <div className="funding-info">
                            <div className="funding-header">
                                <span>Funding Progress</span>
                                <span>{fundingPercentage.toFixed(1)}%</span>
                            </div>
                            <div className="funding-bar">
                                <div 
                                    className="funding-progress"
                                    style={{ width: `${Math.min(fundingPercentage, 100)}%` }}
                                />
                            </div>
                            <div className="funding-details">
                                <span>{formatCurrency(reactor.current_funding)} raised</span>
                                <span>of {formatCurrency(reactor.total_funding_needed)}</span>
                            </div>
                        </div>
                    </>
                )}

                {variant === 'portfolio' && investmentAmount && (
                    <div className="investment-info">
                        <div className="investment-stat">
                            <span>Your Investment</span>
                            <strong>{formatCurrency(investmentAmount)}</strong>
                        </div>
                    </div>
                )}

                <button 
                    className={`btn-invest ${isFullyFunded ? 'disabled' : ''}`}
                    onClick={() => onInvestClick(reactor)}
                    disabled={isFullyFunded}
                >
                    {isFullyFunded ? '✓ Fully Funded' : '⚡ Invest Now'}
                </button>
            </div>
        </div>
    );
};