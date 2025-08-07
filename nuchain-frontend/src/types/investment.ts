import type { Reactor } from './reactor';

export interface Investment {
    id: number;
    user: string;
    reactor: Reactor;
    amount_invested: number;
    created_at: string;
}

export interface PortfolioProjection {
    time_period_years: number;
    total_roi: number;
    total_carbon_offset: number;
    total_return: number;
    roi_percentage: number;
}

export interface PortfolioSummary {
    total_invested: number;
    investment_count: number;
    reactors_invested_in: string[];
    projections: PortfolioProjection[];
}

export interface CreateInvestmentData {
    reactor_id: number;
    amount_invested: number;
}