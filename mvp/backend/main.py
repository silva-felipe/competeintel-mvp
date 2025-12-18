"""
CompeteIntel API - Brazilian Competitor Intelligence Platform
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
import os
from typing import Optional
from sqlalchemy.orm import Session

from models.schemas import (
    CompetitorSearchRequest,
    CompetitorSearchResponse,
    HealthResponse,
    DemoRequestCreate,
    DemoRequestResponse
)
from models.database import init_db, get_db
from services.competitor_service import search_competitors
from services.analysis_service import generate_analytics
from services.cnpj_service import validate_cnpj, format_cnpj, lookup_cnpj
from services.demo_service import process_demo_request, get_demo_request

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() == "true"
API_TITLE = os.getenv("API_TITLE", "CompeteIntel API")
API_VERSION = os.getenv("API_VERSION", "1.0.0")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:8080,http://localhost:8081").split(",")

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description="API de Inteligência Competitiva para o Mercado Brasileiro",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database initialization
@app.on_event("startup")
def startup_db():
    """Initialize database on startup"""
    init_db()


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": API_TITLE,
        "version": API_VERSION,
        "status": "online",
        "docs": "/api/docs",
        "environment": ENVIRONMENT,
        "using_mock_data": USE_MOCK_DATA
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=API_VERSION,
        environment=ENVIRONMENT,
        using_mock_data=USE_MOCK_DATA
    )


@app.post("/api/search", response_model=CompetitorSearchResponse, tags=["Competitors"])
async def search_competitor_analysis(request: CompetitorSearchRequest):
    """
    Search for competitors and generate competitive intelligence analysis
    
    This endpoint:
    1. Searches for competitors based on location and business category
    2. Calculates market density and saturation metrics
    3. Analyzes competitive positioning (if your business data provided)
    4. Estimates market share distribution
    5. Generates actionable KPI recommendations
    
    **Example Request:**
    ```json
    {
        "business_name": "Minha Padaria",
        "category": "Padaria",
        "city": "São Paulo",
        "state": "SP",
        "radius_km": 5.0,
        "max_results": 10
    }
    ```
    """
    try:
        # Search for competitors
        competitors = search_competitors(
            category=request.category.value,
            city=request.city,
            coordinates=request.coordinates,
            radius_km=request.radius_km,
            max_results=request.max_results,
            neighborhood=request.neighborhood,
            cep=request.cep
        )
        
        # Note: Empty results are valid - filters might be too restrictive
        # Don't raise 404, just return empty list with message in analytics
        
        # Generate analytics
        # Note: For now, we don't have "your business" data
        # In a full implementation, this would come from user's profile or be included in request
        your_business = None
        if request.business_name:
            # Mock "your business" data for demonstration
            # In production, this would come from the database or be part of the request
            your_business = {
                "name": request.business_name,
                "rating": 4.2,
                "review_count": 87,
                "online_presence": {
                    "has_website": False,
                    "has_instagram": True,
                    "has_facebook": True,
                    "instagram_followers": 1500,
                    "facebook_likes": 800
                },
                "estimated_monthly_revenue": 45000,
                "has_delivery": True,
                "accepts_pix": True
            }
        
        analytics = generate_analytics(
            competitors=competitors,
            radius_km=request.radius_km,
            your_business=your_business
        )
        
        # Build response
        response = CompetitorSearchResponse(
            query=request,
            competitors=competitors,
            analytics=analytics,
            total_found=len(competitors),
            search_radius_km=request.radius_km
        )
        
        return response
        
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@app.get("/api/cnpj/{cnpj}", tags=["CNPJ"])
async def get_cnpj_info(cnpj: str):
    """
    Look up CNPJ information
    
    **Note:** Currently returns mock data. Real implementation would integrate with
    Receita Federal API or commercial CNPJ data providers.
    
    **Example:** /api/cnpj/12.345.678/0001-90
    """
    # Validate CNPJ
    if not validate_cnpj(cnpj):
        raise HTTPException(
            status_code=400,
            detail="CNPJ inválido. Verifique o formato e dígitos verificadores."
        )
    
    # Look up CNPJ data
    cnpj_data = lookup_cnpj(cnpj)
    
    if not cnpj_data:
        raise HTTPException(
            status_code=404,
            detail="CNPJ não encontrado na base de dados."
        )
    
    return cnpj_data


@app.get("/api/categories", tags=["Metadata"])
async def get_categories():
    """Get list of supported business categories"""
    from data.mock_competitors import BUSINESS_CATEGORIES
    
    categories = []
    for name, data in BUSINESS_CATEGORIES.items():
        categories.append({
            "name": name,
            "cnae_code": data["cnae"],
            "description": data["description"]
        })
    
    return {"categories": categories}


@app.get("/api/cities", tags=["Metadata"])
async def get_cities():
    """Get list of supported cities"""
    from data.mock_competitors import CITIES
    
    cities = []
    for name, data in CITIES.items():
        cities.append({
            "name": name,
            "state": data["state"],
            "coordinates": {
                "latitude": data["lat"],
                "longitude": data["lng"]
            }
        })
    
    return {"cities": cities}


@app.post("/api/demo-request", response_model=DemoRequestResponse, tags=["Demo"])
async def create_demo_request(request: DemoRequestCreate, db: Session = Depends(get_db)):
    """
    Create a demo request from the landing page
    
    This endpoint:
    1. Stores the demo request in the database
    2. Triggers a competitor analysis
    3. Sends the analysis results via email
    4. Returns the request status
    
    **Example Request:**
    ```json
    {
        "business_name": "Padaria da Vila",
        "email": "contato@padariadavila.com.br",
        "city": "São Paulo",
        "state": "SP",
        "category": "Padaria"
    }
    ```
    """
    try:
        response = await process_demo_request(request, db)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar solicitação: {str(e)}")


@app.get("/api/demo-request/{request_id}", tags=["Demo"])
async def get_demo_request_status(request_id: str, db: Session = Depends(get_db)):
    """
    Get the status and results of a demo request
    
    **Example:** /api/demo-request/123e4567-e89b-12d3-a456-426614174000
    """
    result = get_demo_request(request_id, db)
    
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Solicitação não encontrada."
        )
    
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if ENVIRONMENT == "development" else False
    )
