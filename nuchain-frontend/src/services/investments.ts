import api from './api';
import { Reactor } from '../types/reactor';
import { Investment, PortfolioSummary, CreateInvestmentData } from '../types/investment';

export const reactorService = {
    async getReactors(): Promise<Reactor[]> {
        const response = await api.get<Reactor[]>('/reactors/');
        return response.data;
    },

    async getReactor(id: number): Promise<Reactor> {
        const response = await api.get<Reactor>(`/reactors/${id}/`);
        return response.data;
    },
};

export const investmentService = {
    async getInvestments(): Promise<Investment[]> {
        const response = await api.get<Investment[]>('/investments/');
        return response.data;
    },

    async createInvestment(data: CreateInvestmentData): Promise<{
        investment: Investment;
        message: string;
        remaining_balance: number;
        amount_invested: number;
    }> {
        const response = await api.post('/investments/', data);
        return response.data;
    },

    async getPortfolioSummary(): Promise<PortfolioSummary> {
        const response = await api.get<PortfolioSummary>('/investments/portfolio_summary/');
        return response.data;
    },
};