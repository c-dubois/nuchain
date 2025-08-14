import React from 'react';
import type { Reactor } from '../../types/reactor';
import { formatCurrency, formatROIRate, formatCarbonOffset, getReactorImage } from '../../utils/helpers';
import './ReactorCard.css';

interface ReactorCardProps {
    reactor: Reactor;
    onInvestClick: (reactor: Reactor) => void;
    variant?: 'browse' | 'portfolio';
    investmentAmount?: number;
    portfolioTotal?: number;
}

export const ReactorCard: React.FC<ReactorCardProps> = ({ 
    reactor, 
    onInvestClick,
    variant = 'browse',
    investmentAmount,
    portfolioTotal
}) => {
    const fundingPercentage = reactor.funding_percentage || 0;
    const isFullyFunded = reactor.is_fully_funded;

    if (variant === 'portfolio' && investmentAmount) {
        return (
            <div className="reactor-card portfolio">
                <div className="portfolio-image-container">
                    <img 
                        src={getReactorImage(reactor.slug)} 
                        alt={reactor.name}
                        className="portfolio-image"
                        onError={(e) => {
                            (e.target as HTMLImageElement).src = `https://picsum.photos/800/600?text=${encodeURIComponent(reactor.name)}`;
                        }}
                    />
                </div>
                
                <div className="portfolio-content">
                    <div className="portfolio-header">
                        <h3 className="portfolio-name">{reactor.name}</h3>
                        <span className="portfolio-type">{reactor.type}</span>
                    </div>
                    
                    <div className="portfolio-stats-grid">
                        <div className="stat-row">
                            <div className="stat-inline">
                                <span className="stat-inline-label">ROI:</span>
                                <span className={`stat-inline-value ${reactor.annual_roi_rate < 0 ? 'negative' : 'positive'}`}>
                                    {formatROIRate(reactor.annual_roi_rate)}
                                </span>
                            </div>
                            <div className="stat-inline">
                                <span className="stat-inline-label">Portfolio:</span>
                                <span className="stat-inline-value">
                                    {((investmentAmount / (portfolioTotal || 1)) * 100).toFixed(1)}%
                                </span>
                            </div>
                        </div>
                        <div className="stat-row">
                            <div className="stat-inline">
                                <span className="stat-inline-label">CO₂:</span>
                                <span className="stat-inline-value">
                                    {formatCarbonOffset(reactor.carbon_offset_tonnes_co2_per_nuc_per_year)}
                                </span>
                            </div>
                            <div className="stat-inline">
                                <span className="stat-inline-label">Your Investment:</span>
                                <span className="stat-inline-value highlight">
                                    {formatCurrency(investmentAmount)}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <button 
                    className={`portfolio-invest-btn ${isFullyFunded ? 'disabled' : ''}`}
                    onClick={() => onInvestClick(reactor)}
                    disabled={isFullyFunded}
                >
                    {isFullyFunded ? '✓ Fully Funded' : '⚡ Invest'}
                </button>
            </div>
        );
    }

    // Original browse variant
    return (
        <div className="reactor-card browse">
            <div className="reactor-image-container">
                <img 
                    src={getReactorImage(reactor.slug)} 
                    alt={reactor.name}
                    className="reactor-image"
                    onError={(e) => {
                        (e.target as HTMLImageElement).src = `https://picsum.photos/800/600?text=${encodeURIComponent(reactor.name)}`;
                    }}
                />
                <div className="reactor-type-badge">{reactor.type}</div>
            </div>

            <div className="reactor-content">
                <h3 className="reactor-name">{reactor.name}</h3>
                <p className="reactor-location">📍 {reactor.location}</p>

                <div className="reactor-stats-card">
                    <div className="stat">
                        <span className="stat-label">Return on Investment (ROI)</span>
                        <span className={`stat-value ${reactor.annual_roi_rate < 0 ? 'negative' : 'positive'}`}>
                            {formatROIRate(reactor.annual_roi_rate)}
                        </span>
                    </div>
                    <div className="stat">
                        <span className="stat-label">Carbon Offset</span>
                        <span className="stat-value carbon-offset-text">
                            <span className="carbon-value">{formatCarbonOffset(reactor.carbon_offset_tonnes_co2_per_nuc_per_year)}</span>
                            <span className="carbon-unit">per $NUC per year</span>
                        </span>
                    </div>
                </div>

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
}