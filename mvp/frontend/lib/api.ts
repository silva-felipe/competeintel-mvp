// API client for backend communication

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface SearchRequest {
    business_name?: string;
    category: string;
    city: string;
    state?: string;
    neighborhood?: string;
    cep?: string;
    radius_km?: number;
    max_results?: number;
}

export interface Coordinates {
    latitude: number;
    longitude: number;
}

export interface Competitor {
    id: string;
    name: string;
    category: string;
    rating: number;
    review_count: number;
    distance_km?: number;
    coordinates: Coordinates;
    address: {
        street: string;
        neighborhood: string;
        city: string;
        state: string;
    };
    phone: string;
    online_presence: {
        has_instagram: boolean;
        has_facebook: boolean;
        has_website: boolean;
    };
    estimated_monthly_revenue: number;
    has_delivery: boolean;
    accepts_pix: boolean;
}

export interface Analytics {
    market_density: {
        total_competitors: number;
        competitors_per_km2: number;
        density_level: string;
        market_saturation_score: number;
    };
    kpi_recommendations: Array<{
        metric: string;
        current_value: string;
        benchmark_value: string;
        recommendation: string;
        priority: string;
    }>;
    summary: string;
}

export interface SearchResponse {
    competitors: Competitor[];
    analytics: Analytics;
    total_found: number;
}

export async function searchCompetitors(request: SearchRequest): Promise<SearchResponse> {
    const response = await fetch(`${API_BASE_URL}/api/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || 'Failed to search competitors');
    }

    return response.json();
}

export async function getCategories() {
    const response = await fetch(`${API_BASE_URL}/api/categories`);
    if (!response.ok) throw new Error('Failed to fetch categories');
    return response.json();
}

export async function getCities() {
    const response = await fetch(`${API_BASE_URL}/api/cities`);
    if (!response.ok) throw new Error('Failed to fetch cities');
    return response.json();
}
