import { CURRENCY_SYMBOL } from './constants';

/**
 * Format a number as currency with $NUC currency symbol
 * e.g., 1234.56 -> "1,234.56 $NUC"
 */
export const formatCurrency = (amount: number): string => {
    return `${amount.toLocaleString('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    })} ${CURRENCY_SYMBOL}`;
};

/**
 * Format a percentage value with specified decimal places
 * e.g., 0.1234 -> "12.34%"
 */
export const formatPercentage = (value: number, decimals: number = 2): string => {
    return `${value.toFixed(decimals)}%`;
};

/**
 * Format ROI rate as a percentage
 * e.g., 0.1234 -> "12.34%"
 */
export const formatROIRate = (rate: number): string => {
    return formatPercentage(rate * 100);
};

/**
 * Format carbon offset in tonnes CO₂
 * e.g., 1.2345 -> "1.23 tonnes CO₂"
 */
export const formatCarbonOffset = (tonnes: number): string => {
    if (tonnes >= 1000) {
        return `${(tonnes / 1000).toFixed(2)}k tonnes CO₂`;
    }
    return `${tonnes.toFixed(2)} tonnes CO₂`;
};

/**
 * Validate investment amount against user balance and reactor funding
 * Returns an object with valid status and optional error message
 */
export const isValidInvestment = (
    amount: number,
    userBalance: number,
    availableFunding: number
): { valid: boolean; error?: string } => {
    if (amount <= 0) {
        return { valid: false, error: 'Investment amount must be greater than 0' };
    }
    if (amount > userBalance) {
        return { valid: false, error: 'Insufficient balance' };
    }
    if (amount > availableFunding) {
        return { valid: false, error: 'Investment exceeds available reactor funding' };
    }
    return { valid: true };
};

/**
 * Get the image URL for a reactor based on its slug
 */
export const getReactorImage = (slug: string): string => {
    const images: Record<string, string> = {
        'nuwave': '/images/nuwave.jpg',
        'phoenix_regenx7': '/images/phoenix.jpg',
        'nexus_core': '/images/nexus.jpg',
        'fermi_iii': '/images/fermi.jpg',
        'helios_fusiondrive': '/images/helios.jpg'
    };
    
    return images[slug] || '/images/reactor-placeholder.jpg';
};