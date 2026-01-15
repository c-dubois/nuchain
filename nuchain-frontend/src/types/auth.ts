export interface User {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    balance: number;
    wallet?: Wallet;
}

export interface Wallet {
    address: string;
    basescan_url: string;
}

export interface AuthTokens {
    access: string;
    refresh: string;
}

export interface LoginCredentials {
    username: string;
    password: string;
}

export interface RegisterData {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    first_name?: string;
    last_name?: string;
}