"""
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class BusinessCategory(str, Enum):
    """Supported business categories"""
    PADARIA = "Padaria"
    RESTAURANTE = "Restaurante"
    FARMACIA = "Farmácia"
    SUPERMERCADO = "Supermercado"
    CAFETERIA = "Cafeteria"
    ACADEMIA = "Academia"
    PET_SHOP = "Pet Shop"
    LANCHONETE = "Lanchonete"


class Coordinates(BaseModel):
    """Geographic coordinates"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class Address(BaseModel):
    """Address information"""
    street: str
    neighborhood: str
    city: str
    state: str
    postal_code: str
    country: str = "Brasil"


class OnlinePresence(BaseModel):
    """Social media and online presence data"""
    has_instagram: bool
    has_facebook: bool
    has_website: bool
    instagram_followers: int = 0
    facebook_likes: int = 0


class CompetitorSearchRequest(BaseModel):
    """Request model for competitor search"""
    business_name: Optional[str] = Field(None, description="Name of your business (optional)")
    category: BusinessCategory = Field(..., description="Business category/type")
    city: str = Field(..., min_length=2, description="City name")
    state: Optional[str] = Field(None, min_length=2, max_length=2, description="State abbreviation (e.g., SP, RJ)")
    neighborhood: Optional[str] = Field(None, description="Neighborhood/bairro for more precise search")
    cep: Optional[str] = Field(None, description="CEP (postal code) for exact location search - format: XXXXX-XXX or 8 digits")
    address: Optional[str] = Field(None, description="Full address (optional)")
    coordinates: Optional[Coordinates] = Field(None, description="Coordinates (if known)")
    radius_km: float = Field(5.0, ge=0.5, le=50, description="Search radius in kilometers")
    max_results: int = Field(10, ge=1, le=50, description="Maximum number of competitors to return")

    @validator('cep')
    def validate_cep(cls, v):
        if v is None or v == "" or v.strip() == "":
            return None  # Empty string becomes None (optional field)
        # Remove formatting
        cep_clean = v.replace("-", "").replace(".", "").replace(" ", "")
        # Must be exactly 8 digits
        if not cep_clean.isdigit() or len(cep_clean) != 8:
            raise ValueError('CEP must be 8 digits in format XXXXX-XXX or 12345678')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "business_name": "Minha Padaria",
                "category": "Padaria",
                "city": "São Paulo",
                "state": "SP",
                "neighborhood": "Vila Madalena",
                "cep": "05435-000",
                "radius_km": 5.0,
                "max_results": 10
            }
        }




class Competitor(BaseModel):
    """Individual competitor information"""
    id: str
    name: str
    category: str
    cnae_code: str
    cnae_description: str
    cnpj: str
    coordinates: Coordinates
    address: Address
    phone: str
    rating: float = Field(..., ge=0, le=5)
    review_count: int = Field(..., ge=0)
    distance_km: Optional[float] = Field(None, description="Distance from your business in km")
    online_presence: OnlinePresence
    is_verified: bool
    opening_year: int
    employee_count_estimate: str
    estimated_monthly_revenue: int
    has_delivery: bool
    accepts_pix: bool
    accepts_cards: bool


class MarketDensityAnalysis(BaseModel):
    """Market density and saturation metrics"""
    total_competitors: int
    competitors_per_km2: float
    density_level: str = Field(..., description="Low, Medium, High, or Very High")
    market_saturation_score: float = Field(..., ge=0, le=100, description="0-100 scale")
    avg_distance_between_competitors: float


class CompetitivePositioning(BaseModel):
    """Where your business stands relative to competitors"""
    your_ranking: int = Field(..., description="Your position if sorted by rating")
    total_competitors: int
    percentile: float = Field(..., ge=0, le=100)
    above_average_rating: bool
    above_average_reviews: bool
    online_presence_score: float = Field(..., ge=0, le=100)


class MarketShareEstimate(BaseModel):
    """Estimated market share based on various factors"""
    your_estimated_share: float = Field(..., ge=0, le=100, description="Percentage")
    top_3_competitors: List[Dict[str, Any]]
    concentration_ratio: float = Field(..., description="CR3 - market share of top 3")
    market_structure: str = Field(..., description="Fragmented, Moderate, or Concentrated")


class KPIRecommendation(BaseModel):
    """Actionable KPI and recommendations"""
    metric: str
    current_value: str
    benchmark_value: str
    recommendation: str
    priority: str = Field(..., description="High, Medium, or Low")
    expected_impact: str


class AnalyticsResponse(BaseModel):
    """Complete analytics and insights"""
    market_density: MarketDensityAnalysis
    competitive_positioning: Optional[CompetitivePositioning] = None
    market_share_estimate: Optional[MarketShareEstimate] = None
    kpi_recommendations: List[KPIRecommendation]
    summary: str


class CompetitorSearchResponse(BaseModel):
    """Response model for competitor search"""
    query: CompetitorSearchRequest
    competitors: List[Competitor]
    analytics: AnalyticsResponse
    total_found: int
    search_radius_km: float

    class Config:
        json_schema_extra = {
            "example": {
                "total_found": 10,
                "search_radius_km": 5.0,
                "competitors": [],
                "analytics": {}
            }
        }


class HealthResponse(BaseModel):
    """API health check response"""
    status: str
    version: str
    environment: str
    using_mock_data: bool


# Demo Request Schemas

class DemoRequestCreate(BaseModel):
    """Request model for landing page demo requests"""
    business_name: str = Field(..., min_length=2, max_length=200, description="Name of the business")
    email: EmailStr = Field(..., description="Email to send analysis results")
    city: str = Field(..., min_length=2, max_length=100, description="City name")
    state: Optional[str] = Field(None, min_length=2, max_length=2, description="State abbreviation (e.g., SP, RJ)")
    category: BusinessCategory = Field(..., description="Business category")

    class Config:
        json_schema_extra = {
            "example": {
                "business_name": "Padaria da Vila",
                "email": "contato@padariadavila.com.br",
                "city": "São Paulo",
                "state": "SP",
                "category": "Padaria"
            }
        }


class DemoRequestResponse(BaseModel):
    """Response model for demo request"""
    id: str
    business_name: str
    email: str
    city: str
    state: Optional[str]
    category: str
    status: str
    created_at: datetime
    message: str = Field(..., description="User-friendly success message")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "business_name": "Padaria da Vila",
                "email": "contato@padariadavila.com.br",
                "city": "São Paulo",
                "state": "SP",
                "category": "Padaria",
                "status": "completed",
                "created_at": "2024-01-15T10:30:00",
                "message": "Análise enviada com sucesso! Verifique seu email."
            }
        }

