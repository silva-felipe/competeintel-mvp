"""
Demo request service - Business logic for handling demo requests
"""

import logging
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session

from models.database import DemoRequest, DemoRequestStatus
from models.schemas import DemoRequestCreate, DemoRequestResponse
from services.competitor_service import search_competitors
from services.analysis_service import generate_analytics
from services.email_service import send_analysis_email

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_demo_request(
    demo_data: DemoRequestCreate,
    db: Session
) -> DemoRequestResponse:
    """
    Process a demo request from the landing page
    
    Steps:
    1. Create database record with status="pending"
    2. Trigger competitor analysis
    3. Update record with results and status="completed"
    4. Send email with analysis results
    5. Return response to user
    
    Args:
        demo_data: Demo request data from landing page
        db: Database session
    
    Returns:
        DemoRequestResponse with request details
    """
    
    # Step 1: Create database record
    db_request = DemoRequest(
        business_name=demo_data.business_name,
        email=demo_data.email,
        city=demo_data.city,
        state=demo_data.state,
        category=demo_data.category.value,
        status=DemoRequestStatus.PENDING
    )
    
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    logger.info("Created demo request: %s for %s", db_request.id, demo_data.email)
    
    try:
        # Step 2: Update status to processing
        db_request.status = DemoRequestStatus.PROCESSING
        db.commit()
        
        # Step 3: Trigger competitor analysis
        logger.info("Starting competitor analysis for %s", demo_data.business_name)
        
        competitors = search_competitors(
            category=demo_data.category.value,
            city=demo_data.city,
            coordinates=None,
            radius_km=5.0,
            max_results=10,
            neighborhood=None,
            cep=None
        )
        
        # Generate analytics
        # Include mock "your business" data for better recommendations
        your_business = {
            "name": demo_data.business_name,
            "rating": 4.2,
            "review_count": 50,
            "online_presence": {
                "has_website": False,
                "has_instagram": True,
                "has_facebook": True,
                "instagram_followers": 1000,
                "facebook_likes": 500
            },
            "estimated_monthly_revenue": 35000,
            "has_delivery": True,
            "accepts_pix": True
        }
        
        analytics = generate_analytics(
            competitors=competitors,
            radius_km=5.0,
            your_business=your_business
        )
        
        # Build analysis results
        # Convert Pydantic models to dicts for JSON storage
        competitors_dict = [comp.model_dump() for comp in competitors]
        analytics_dict = {
            "market_density": analytics.market_density.model_dump(),
            "competitive_positioning": analytics.competitive_positioning.model_dump() if analytics.competitive_positioning else None,
            "market_share_estimate": analytics.market_share_estimate.model_dump() if analytics.market_share_estimate else None,
            "kpi_recommendations": [kpi.model_dump() for kpi in analytics.kpi_recommendations],
            "summary": analytics.summary
        }
        
        analysis_results = {
            "competitors": competitors_dict,
            "analytics": analytics_dict,
            "total_found": len(competitors),
            "search_radius_km": 5.0
        }
        
        logger.info("Analysis completed: found %d competitors", len(competitors))
        
        # Step 4: Store results in database
        db_request.analysis_results = analysis_results
        db_request.status = DemoRequestStatus.COMPLETED
        db_request.updated_at = datetime.utcnow()
        db.commit()
        
        # Step 5: Send email with results
        logger.info("Sending analysis email to %s", demo_data.email)
        
        email_sent = await send_analysis_email(
            to_email=demo_data.email,
            business_name=demo_data.business_name,
            city=demo_data.city,
            state=demo_data.state or "",
            category=demo_data.category.value,
            analysis_results=analysis_results
        )
        
        if not email_sent:
            logger.warning("Email sending failed, but request completed successfully")
        
        # Step 6: Return success response
        message = f"Análise enviada com sucesso! Encontramos {len(competitors)} concorrentes em {demo_data.city}. Verifique seu email {demo_data.email} para ver os detalhes."
        
        return DemoRequestResponse(
            id=db_request.id,
            business_name=db_request.business_name,
            email=db_request.email,
            city=db_request.city,
            state=db_request.state,
            category=db_request.category,
            status=db_request.status.value,
            created_at=db_request.created_at,
            message=message
        )
        
    except Exception as e:
        # Handle errors: update status to failed
        logger.error("Error processing demo request: %s", str(e))
        
        db_request.status = DemoRequestStatus.FAILED
        db_request.error_message = str(e)
        db_request.updated_at = datetime.utcnow()
        db.commit()
        
        # Still return a response, but with error status
        return DemoRequestResponse(
            id=db_request.id,
            business_name=db_request.business_name,
            email=db_request.email,
            city=db_request.city,
            state=db_request.state,
            category=db_request.category,
            status=db_request.status.value,
            created_at=db_request.created_at,
            message=f"Houve um erro ao processar sua solicitação. Por favor, tente novamente mais tarde ou entre em contato conosco."
        )


def get_demo_request(request_id: str, db: Session) -> Dict[str, Any]:
    """
    Get a demo request by ID (for admin or user to check status)
    
    Args:
        request_id: Demo request ID
        db: Database session
    
    Returns:
        Demo request details including analysis results
    """
    
    db_request = db.query(DemoRequest).filter(DemoRequest.id == request_id).first()
    
    if not db_request:
        return None
    
    return {
        "id": db_request.id,
        "business_name": db_request.business_name,
        "email": db_request.email,
        "city": db_request.city,
        "state": db_request.state,
        "category": db_request.category,
        "status": db_request.status.value,
        "created_at": db_request.created_at,
        "updated_at": db_request.updated_at,
        "analysis_results": db_request.analysis_results,
        "error_message": db_request.error_message
    }


def list_demo_requests(db: Session, limit: int = 50) -> list:
    """
    List all demo requests (admin endpoint)
    
    Args:
        db: Database session
        limit: Maximum number of requests to return
    
    Returns:
        List of demo requests
    """
    
    requests = db.query(DemoRequest).order_by(DemoRequest.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": req.id,
            "business_name": req.business_name,
            "email": req.email,
            "city": req.city,
            "category": req.category,
            "status": req.status.value,
            "created_at": req.created_at
        }
        for req in requests
    ]
