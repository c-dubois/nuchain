export const TIME_PERIODS = [1, 2, 5, 10] as const;
export type TimePeriod = typeof TIME_PERIODS[number];

// Initial user balance
export const INITIAL_BALANCE = 25000;

// Currency symbol
export const CURRENCY_SYMBOL = '$NUC';

// Reactor slugs (matching backend)
export const REACTOR_SLUGS = {
    NUWAVE: 'nuwave',
    PHOENIX: 'phoenix_regenx7',
    NEXUS: 'nexus_core',
    FERMI: 'fermi_iii',
    HELIOS: 'helios_fusiondrive',
    ATUCHA: 'atucha_qtronix'
} as const;

// Investment limits
export const MIN_INVESTMENT = 1;
export const MAX_INVESTMENT_PERCENTAGE = 100; // Max % of balance you can invest at once

// Chart colors for data visualization
export const CHART_COLORS = {
  roi: '#daff02',        // Primary color for ROI
  carbon: '#685bc7',     // Accent color for carbon offset
  gridColor: '#f3f0eb',  // Medium color for grid lines
  textColor: '#f3f0eb'   // Light color for text
};

export const PIE_COLORS = ['#daff02', '#fe572a', '#685bc7', '#4CC9F0', '#fd3f95ff', '#40f476ff'];