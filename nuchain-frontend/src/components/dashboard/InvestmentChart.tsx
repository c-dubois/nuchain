import React from 'react';
import {
    LineChart,
    Line,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer
} from 'recharts';
import type { PortfolioSummary } from '../../types/investment';
import { CHART_COLORS } from '../../utils/constants';
import { formatCurrency, formatCarbonOffset } from '../../utils/helpers';
import './InvestmentChart.css';

interface InvestmentChartProps {
    summary: PortfolioSummary | null;
    chartType?: 'line' | 'bar';
}

export const InvestmentChart: React.FC<InvestmentChartProps> = ({
    summary,
    chartType = 'line'
}) => {
    if (!summary || summary.investment_count === 0) {
        return null;
    }

    // Transform data for Recharts
    const chartData = summary.projections.map((projection) => ({
        period: `${projection.time_period_years}Y`,
        roi: projection.total_roi,
        carbonOffset: projection.total_carbon_offset,
        totalReturn: projection.total_return
    }));

    const CustomTooltip = ({ active, payload }: any) => {
        if (active && payload && payload.length) {
            return (
                <div className="chart-tooltip">
                    <p className="tooltip-label">{payload[0].payload.period}</p>
                    {payload.map((entry: any, index: number) => (
                        <p key={index} className="tooltip-item" style={{ color: entry.color }}>
                            {entry.name}: {
                                entry.dataKey === 'carbonOffset' 
                                    ? formatCarbonOffset(entry.value)
                                    : formatCurrency(entry.value)
                            }
                        </p>
                    ))}
                </div>
            );
        }
        return null;
    };

    return (
        <div className="investment-chart">
            <h3>Investment Projections</h3>
        
            <div className="chart-container">
                <ResponsiveContainer width="100%" height={300}>
                    {chartType === 'line' ? (
                        <LineChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" stroke={CHART_COLORS.gridColor} />
                            <XAxis 
                                dataKey="period" 
                                stroke={CHART_COLORS.textColor}
                            />
                            <YAxis 
                                stroke={CHART_COLORS.textColor}
                                tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
                            />
                            <Tooltip content={<CustomTooltip />} />
                            <Legend />
                            <Line
                                type="monotone"
                                dataKey="totalReturn"
                                name="Total Return"
                                stroke={CHART_COLORS.roi}
                                strokeWidth={3}
                                dot={{ fill: CHART_COLORS.roi, r: 6 }}
                                activeDot={{ r: 8 }}
                            />
                            <Line
                                type="monotone"
                                dataKey="roi"
                                name="ROI"
                                stroke={CHART_COLORS.carbon}
                                strokeWidth={3}
                                dot={{ fill: CHART_COLORS.carbon, r: 6 }}
                                activeDot={{ r: 8 }}
                            />
                        </LineChart>
                    ) : (
                        <BarChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" stroke={CHART_COLORS.gridColor} />
                            <XAxis 
                                dataKey="period" 
                                stroke={CHART_COLORS.textColor}
                            />
                            <YAxis 
                                stroke={CHART_COLORS.textColor}
                                tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
                            />
                            <Tooltip content={<CustomTooltip />} />
                            <Legend />
                            <Bar
                                dataKey="totalReturn"
                                name="Total Return"
                                fill={CHART_COLORS.roi}
                            />
                            <Bar
                                dataKey="roi"
                                name="ROI"
                                fill={CHART_COLORS.carbon}
                            />
                        </BarChart>
                    )}
                </ResponsiveContainer>
            </div>

            <div className="chart-carbon">
                <h4>Carbon Offset Projection</h4>
                <ResponsiveContainer width="100%" height={200}>
                    <BarChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke={CHART_COLORS.gridColor} />
                        <XAxis 
                            dataKey="period" 
                            stroke={CHART_COLORS.textColor}
                        />
                        <YAxis 
                            stroke={CHART_COLORS.textColor}
                            tickFormatter={(value) => `${value.toFixed(0)}t`}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Bar
                            dataKey="carbonOffset"
                            name="CO₂ Offset (tonnes)"
                            fill={CHART_COLORS.carbon}
                        />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};