import React, { useState, useEffect } from 'react';
import type { Reactor } from '../../types/reactor';
import { useAuth } from '../../hooks/useAuth';
import { formatCurrency, formatROIRate, isValidInvestment } from '../../utils/helpers';
import './InvestmentModal.css';

interface InvestmentModalProps {
    reactor: Reactor | null;
    isOpen: boolean;
    onClose: () => void;
    onInvest: (reactorId: number, amount: number) => Promise<void>;
}

export const InvestmentModal: React.FC<InvestmentModalProps> = ({
    reactor,
    isOpen,
    onClose,
    onInvest
}) => {
    const { user } = useAuth();
    const [amount, setAmount] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (!isOpen) {
            setAmount('');
            setError('');
        }
    }, [isOpen]);

    if (!isOpen || !reactor || !user) return null;

    const handleAmountChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        if (value === '' || /^\d+\.?\d*$/.test(value)) {
            setAmount(value);
            setError('');
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        const investmentAmount = parseFloat(amount);
        
        const validation = isValidInvestment(
            investmentAmount,
            user.balance,
            reactor.available_funding
        );

        if (!validation.valid) {
            setError(validation.error || 'Invalid investment amount');
            return;
        }

        setLoading(true);
        try {
            await onInvest(reactor.id, investmentAmount);
            onClose();
        } catch {
            setError('Failed to process investment. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const setPercentage = (percentage: number) => {
        const maxAmount = Math.min(user.balance, reactor.available_funding);
        const calculatedAmount = (maxAmount * percentage) / 100;
        setAmount(calculatedAmount.toFixed(2));
        setError('');
    };

    const investmentAmount = parseFloat(amount) || 0;
    const projectedROI = investmentAmount * reactor.annual_roi_rate;
    const projectedCarbonOffset = investmentAmount * reactor.carbon_offset_tonnes_co2_per_nuc_per_year;

    return (
        <>
            <div className="modal-overlay" onClick={onClose} />
            <div className="investment-modal">
                <div className="modal-header">
                    <h2>Invest in {reactor.name}</h2>
                    <button className="modal-close" onClick={onClose}>×</button>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className="modal-body">
                        <div className="investment-summary">
                            <div className="summary-item">
                                <span>Your Balance:</span>
                                <strong>{formatCurrency(user.balance)}</strong>
                            </div>
                            <div className="summary-item">
                                <span>Available to Invest:</span>
                                <strong>{formatCurrency(reactor.available_funding)}</strong>
                            </div>
                            <div className="summary-item">
                                <span>Annual ROI Rate:</span>
                                <strong className={reactor.annual_roi_rate < 0 ? 'negative' : 'positive'}>
                                    {formatROIRate(reactor.annual_roi_rate)}
                                </strong>
                            </div>
                        </div>

                        <div className="investment-input-group">
                            <label htmlFor="amount">Investment Amount ($NUC)</label>
                            <input
                                id="amount"
                                type="text"
                                value={amount}
                                onChange={handleAmountChange}
                                placeholder="Enter amount"
                                className="investment-input"
                                autoFocus
                            />

                            <p className="percentage-label">
                                Or select a percentage of your available funds to invest:
                            </p>

                            <div className="percentage-buttons">
                                <button type="button" onClick={() => setPercentage(25)}>25%</button>
                                <button type="button" onClick={() => setPercentage(50)}>50%</button>
                                <button type="button" onClick={() => setPercentage(75)}>75%</button>
                                <button type="button" onClick={() => setPercentage(100)}>MAX</button>
                            </div>
                        </div>

                        {amount && investmentAmount > 0 && (
                            <div className="investment-preview">
                                <h4>Annual Projections:</h4>
                                <div className="preview-item">
                                    <span>Expected ROI:</span>
                                    <strong className={projectedROI < 0 ? 'negative' : 'positive'}>
                                        {formatCurrency(projectedROI)}
                                    </strong>
                                </div>
                                <div className="preview-item">
                                    <span>Carbon Offset:</span>
                                    <strong>{projectedCarbonOffset.toFixed(2)} tonnes CO₂</strong>
                                </div>
                            </div>
                        )}

                        {error && <div className="error-message">{error}</div>}
                    </div>

                    <div className="modal-footer">
                        <button
                            type="button"
                            className="btn-secondary"
                            onClick={onClose}
                            disabled={loading}
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="btn-primary"
                            disabled={loading || !amount || investmentAmount <= 0}
                        >
                            {loading ? 'Processing...' : `Invest ${amount ? formatCurrency(investmentAmount) : ''}`}
                        </button>
                    </div>
                </form>
            </div>
        </>
    );
};