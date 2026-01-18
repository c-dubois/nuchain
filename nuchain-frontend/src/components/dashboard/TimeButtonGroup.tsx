import React from 'react';
import { TIME_PERIODS, type TimePeriod } from '../../utils/constants';
import './TimeButtonGroup.css';

interface TimeButtonGroupProps {
    selectedPeriod: TimePeriod;
    onPeriodChange: (period: TimePeriod) => void;
}

export const TimeButtonGroup: React.FC<TimeButtonGroupProps> = ({
    selectedPeriod,
    onPeriodChange
}) => {
    return (
        <div className="time-button-group">
            <div className="time-button-content">
                <span className="time-label">Time Period:</span>
                <div className="time-buttons">
                    {TIME_PERIODS.map((period) => (
                        <button
                            key={period}
                            className={`time-button ${selectedPeriod === period ? 'active' : ''}`}
                            onClick={() => onPeriodChange(period)}
                        >
                            {period} {period === 1 ? 'Year' : 'Years'}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
};