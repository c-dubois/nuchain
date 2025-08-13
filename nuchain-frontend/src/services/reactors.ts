import api from './api';
import type { Reactor } from '../types/reactor';

export const reactorService = {
    async getReactors(): Promise<Reactor[]> {
        const response = await api.get<{ results: Reactor[] }>('/reactors/');
        return response.data.results;
    },

    async getReactor(id: number): Promise<Reactor> {
        const response = await api.get<Reactor>(`/reactors/${id}/`);
        return response.data;
    },
};