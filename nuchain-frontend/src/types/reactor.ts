export interface Reactor {
    id: number;
    name: string;
    slug: string;
    type: string;
    description: string;
    location: string;
    annual_roi_rate: number;
    carbon_offset_tonnes_co2_per_nuc_per_year: number;
    total_funding_needed: number;
    current_funding: number;
    funding_percentage: number;
    available_funding: number;
    is_fully_funded: boolean;
    is_active: boolean;
    created_at: string;
}