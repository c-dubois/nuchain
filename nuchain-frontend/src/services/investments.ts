import api from './api';
import type { Investment, PortfolioSummary, CreateInvestmentData } from '../types/investment';

export const investmentService = {
    async getInvestments(): Promise<Investment[]> {
        const response = await api.get<{ results: Investment[] }>('/investments/');
        return response.data.results;
    },
    
    async createInvestment(data: CreateInvestmentData): Promise<{
        investment: Investment;
        message: string;
        remaining_balance: number;
        amount_invested: number;
        tx_hash: string;
        tx_url: string;
    }> {
        const response = await api.post('/investments/', data);
        return response.data;
    },
    
    async getPortfolioSummary(): Promise<PortfolioSummary> {
        const response = await api.get<PortfolioSummary>('/investments/portfolio_summary/');
        return response.data;
    },
};