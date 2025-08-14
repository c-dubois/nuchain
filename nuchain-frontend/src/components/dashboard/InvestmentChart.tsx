import React from 'react';
import {
    LineChart,
    Line,
    BarChart,
    Bar,
    PieChart,
    Pie,
    Cell,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer
} from 'recharts';
import type { PortfolioSummary } from '../../types/investment';
import type { Investment } from '../../types/investment';
import { CHART_COLORS, PIE_COLORS } from '../../utils/constants';
import { formatCurrency, formatPercentage, formatCarbonOffset } from '../../utils/helpers';
import './InvestmentChart.css';

interface TooltipPayload {
    color?: string;
    value?: number;
    dataKey?: string;
    name?: string;
    payload?: {
        period: string;
        roi: number;
        carbonOffset: number;
        totalReturn: number;
    };
}

interface InvestmentChartProps {
    summary: PortfolioSummary | null;
    chartType?: 'line' | 'bar' | 'pie';
    investments?: Investment[];
}

export const InvestmentChart: React.FC<InvestmentChartProps> = ({
    summary,
    investments
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

    const pieData = investments?.map((inv) => ({
        name: inv.reactor.name,
        value: parseFloat(inv.amount_invested.toString()),
        percentage: formatPercentage((parseFloat(inv.amount_invested.toString()) / parseFloat(summary.total_invested.toString())) * 100)
    })) || [];

    const CustomTooltip = ({ 
        active, 
        payload 
    }: {
        active?: boolean;
        payload?: TooltipPayload[];
    }) => {
        if (active && payload && payload.length) {
            return (
                <div className="chart-tooltip">
                    <p className="tooltip-label">{payload[0]?.payload?.period}</p>
                    {payload.map((entry, index) => (
                        <p key={index} className="tooltip-item" style={{ color: entry.color }}>
                            {entry.name}: {
                                entry.dataKey === 'carbonOffset' 
                                    ? formatCarbonOffset(entry.value || 0)
                                    : formatCurrency(entry.value || 0)
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
            <h3 className='investment-chart-title'>Investment Projections</h3>

            <div className="chart-container">
                <ResponsiveContainer width="100%" height={300}>
                        <LineChart 
                            data={chartData}
                            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                        >
                            <CartesianGrid strokeDasharray="3 3" stroke={CHART_COLORS.gridColor} />
                            <XAxis 
                                dataKey="period" 
                                tickMargin={5}
                                stroke={CHART_COLORS.textColor}
                            />
                            <YAxis 
                                stroke={CHART_COLORS.textColor}
                                tickMargin={10}
                                tickFormatter={(value) => `${(value / 1000).toFixed(0)}k $NUC`}
                            />
                            <Tooltip content={<CustomTooltip />} />
                            <Legend />
                            <Line
                                type="monotone"
                                dataKey="totalReturn"
                                name="Total Investment Value"
                                stroke={CHART_COLORS.carbon}
                                strokeWidth={3}
                                dot={{ fill: CHART_COLORS.carbon, r: 6 }}
                                activeDot={{ r: 8 }}
                            />
                            <Line
                                type="monotone"
                                dataKey="roi"
                                name="Return on Investment (ROI)"
                                stroke={CHART_COLORS.roi}
                                strokeWidth={3}
                                dot={{ fill: CHART_COLORS.roi, r: 6 }}
                                activeDot={{ r: 8 }}
                            />
                        </LineChart>
                </ResponsiveContainer>
            </div>

            <div className="chart-carbon">
                <h3 className='carbon-offset-title'>Carbon Offset Projections</h3>
                <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke={CHART_COLORS.gridColor} />
                        <XAxis 
                            dataKey="period" 
                            stroke={CHART_COLORS.textColor}
                        />
                        <YAxis 
                            stroke={CHART_COLORS.textColor}
                            tickMargin={10}
                            tickFormatter={(value) => `${(value / 1000).toFixed(0)}k t`}
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

            <div className="chart-portfolio">
                <h3 className='portfolio-distribution-title'>Portfolio Distribution</h3>
                <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                        <Pie
                            data={pieData}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={({ percentage }) => `${percentage}`}
                            outerRadius={85}
                            fill="#8884d8"
                            dataKey="value"
                        >
                            {pieData.map((_entry, index) => (
                                <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                            ))}
                        </Pie>
                        <Tooltip formatter={(value) => formatCurrency(value as number)} />
                        <Legend />
                    </PieChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};