"""
Business analysis service for competitive intelligence
"""

from typing import List, Dict, Optional
from models.schemas import (
    Competitor,
    MarketDensityAnalysis,
    CompetitivePositioning,
    MarketShareEstimate,
    KPIRecommendation,
    AnalyticsResponse
)
import math


def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate distance between two coordinates using Haversine formula
    Returns distance in kilometers
    """
    R = 6371  # Earth's radius in km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


def analyze_market_density(
    competitors: List[Competitor],
    radius_km: float
) -> MarketDensityAnalysis:
    """Analyze market density and saturation"""
    total_competitors = len(competitors)
    area_km2 = math.pi * (radius_km ** 2)
    competitors_per_km2 = total_competitors / area_km2 if area_km2 > 0 else 0
    
    # Determine density level
    if competitors_per_km2 < 0.5:
        density_level = "Low"
        saturation_score = min(competitors_per_km2 * 40, 25)
    elif competitors_per_km2 < 1.5:
        density_level = "Medium"
        saturation_score = 25 + min((competitors_per_km2 - 0.5) * 30, 25)
    elif competitors_per_km2 < 3.0:
        density_level = "High"
        saturation_score = 50 + min((competitors_per_km2 - 1.5) * 20, 30)
    else:
        density_level = "Very High"
        saturation_score = min(80 + (competitors_per_km2 - 3.0) * 5, 100)
    
    # Calculate average distance between competitors
    if total_competitors > 1:
        distances = []
        for i, comp1 in enumerate(competitors):
            for comp2 in competitors[i+1:]:
                dist = calculate_distance(
                    comp1.coordinates.latitude,
                    comp1.coordinates.longitude,
                    comp2.coordinates.latitude,
                    comp2.coordinates.longitude
                )
                distances.append(dist)
        avg_distance = sum(distances) / len(distances) if distances else 0
    else:
        avg_distance = radius_km * 2  # Approximate if only one or none
    
    return MarketDensityAnalysis(
        total_competitors=total_competitors,
        competitors_per_km2=round(competitors_per_km2, 2),
        density_level=density_level,
        market_saturation_score=round(saturation_score, 1),
        avg_distance_between_competitors=round(avg_distance, 2)
    )


def analyze_competitive_positioning(
    your_business: Optional[Dict],
    competitors: List[Competitor]
) -> Optional[CompetitivePositioning]:
    """Analyze competitive positioning (if user provides their business data)"""
    if not your_business:
        return None
    
    # Get your metrics
    your_rating = your_business.get("rating", 4.0)
    your_reviews = your_business.get("review_count", 50)
    your_online = your_business.get("online_presence", {})
    
    # Calculate where you rank
    ratings = [c.rating for c in competitors] + [your_rating]
    sorted_ratings = sorted(ratings, reverse=True)
    your_ranking = sorted_ratings.index(your_rating) + 1
    total = len(sorted_ratings)
    
    # Calculate percentile
    percentile = ((total - your_ranking) / total) * 100 if total > 0 else 0
    
    # Compare to average
    avg_rating = sum(c.rating for c in competitors) / len(competitors) if competitors else 4.0
    avg_reviews = sum(c.review_count for c in competitors) / len(competitors) if competitors else 100
    
    # Calculate online presence score
    online_score = 0
    if your_online.get("has_website"):
        online_score += 40
    if your_online.get("has_instagram"):
        online_score += 30
        # Bonus for followers
        followers = your_online.get("instagram_followers", 0)
        online_score += min(followers / 1000, 20)
    if your_online.get("has_facebook"):
        online_score += 10
    
    online_score = min(online_score, 100)
    
    return CompetitivePositioning(
        your_ranking=your_ranking,
        total_competitors=total,
        percentile=round(percentile, 1),
        above_average_rating=your_rating > avg_rating,
        above_average_reviews=your_reviews > avg_reviews,
        online_presence_score=round(online_score, 1)
    )


def estimate_market_share(
    your_business: Optional[Dict],
    competitors: List[Competitor]
) -> Optional[MarketShareEstimate]:
    """Estimate market share based on revenue estimates"""
    if not competitors:
        return None
    
    # Sort by revenue
    sorted_comps = sorted(competitors, key=lambda x: x.estimated_monthly_revenue, reverse=True)
    
    # Get top 3
    top_3 = []
    total_market_revenue = sum(c.estimated_monthly_revenue for c in competitors)
    
    if your_business:
        total_market_revenue += your_business.get("estimated_monthly_revenue", 0)
    
    for i, comp in enumerate(sorted_comps[:3]):
        share = (comp.estimated_monthly_revenue / total_market_revenue * 100) if total_market_revenue > 0 else 0
        top_3.append({
            "name": comp.name,
            "estimated_revenue": comp.estimated_monthly_revenue,
            "market_share": round(share, 1)
        })
    
    # Calculate concentration ratio (CR3)
    top_3_revenue = sum(c.estimated_monthly_revenue for c in sorted_comps[:3])
    cr3 = (top_3_revenue / total_market_revenue * 100) if total_market_revenue > 0 else 0
    
    # Determine market structure
    if cr3 < 40:
        market_structure = "Fragmented"  # No clear leaders
    elif cr3 < 70:
        market_structure = "Moderate"  # Some concentration
    else:
        market_structure = "Concentrated"  # Dominated by top players
    
    # Calculate your share if provided
    your_share = 0
    if your_business and total_market_revenue > 0:
        your_revenue = your_business.get("estimated_monthly_revenue", 0)
        your_share = (your_revenue / total_market_revenue) * 100
    
    return MarketShareEstimate(
        your_estimated_share=round(your_share, 1),
        top_3_competitors=top_3,
        concentration_ratio=round(cr3, 1),
        market_structure=market_structure
    )


def generate_kpi_recommendations(
    your_business: Optional[Dict],
    competitors: List[Competitor],
    market_density: MarketDensityAnalysis,
    positioning: Optional[CompetitivePositioning]
) -> List[KPIRecommendation]:
    """Generate actionable KPI recommendations"""
    recommendations = []
    
    if not competitors:
        return recommendations
    
    # Calculate benchmarks
    avg_rating = sum(c.rating for c in competitors) / len(competitors)
    avg_reviews = sum(c.review_count for c in competitors) / len(competitors)
    pct_with_instagram = sum(1 for c in competitors if c.online_presence.has_instagram) / len(competitors) * 100
    pct_with_website = sum(1 for c in competitors if c.online_presence.has_website) / len(competitors) * 100
    pct_with_delivery = sum(1 for c in competitors if c.has_delivery) / len(competitors) * 100
    pct_accepts_pix = sum(1 for c in competitors if c.accepts_pix) / len(competitors) * 100
    
    # Rating recommendation
    if your_business:
        your_rating = your_business.get("rating", 0)
        if your_rating < avg_rating:
            recommendations.append(KPIRecommendation(
                metric="Avaliação Google",
                current_value=f"{your_rating:.1f} estrelas",
                benchmark_value=f"{avg_rating:.1f} estrelas (média)",
                recommendation="Foque em melhorar a experiência do cliente e incentive avaliações positivas. Considere programa de fidelidade.",
                priority="High",
                expected_impact="Aumento de 30-50% em novas visitas"
            ))
        
        your_reviews = your_business.get("review_count", 0)
        if your_reviews < avg_reviews:
            recommendations.append(KPIRecommendation(
                metric="Número de Avaliações",
                current_value=f"{your_reviews} avaliações",
                benchmark_value=f"{int(avg_reviews)} avaliações (média)",
                recommendation="Peça feedback ativamente. Use QR codes, incentivos e follow-up pós-venda.",
                priority="Medium",
                expected_impact="Maior credibilidade e visibilidade online"
            ))
        
        has_instagram = your_business.get("online_presence", {}).get("has_instagram", False)
        if not has_instagram and pct_with_instagram > 50:
            recommendations.append(KPIRecommendation(
                metric="Presença no Instagram",
                current_value="Não ativo",
                benchmark_value=f"{pct_with_instagram:.0f}% dos concorrentes têm",
                recommendation="Crie perfil no Instagram e poste regularmente (3-5x/semana). Foco em conteúdo visual atrativo.",
                priority="High",
                expected_impact="Acesso a 58% dos brasileiros ativos na plataforma"
            ))
    
    # Market-level recommendations
    if market_density.market_saturation_score > 70:
        recommendations.append(KPIRecommendation(
            metric="Saturação de Mercado",
            current_value=f"{market_density.market_saturation_score:.0f}/100",
            benchmark_value="<50 ideal",
            recommendation="Mercado muito saturado. Diferencie-se: nicho específico, produto único ou excelência em atendimento.",
            priority="High",
            expected_impact="Diferenciação é crítica para sobrevivência"
        ))
    
    # Delivery recommendation
    if pct_with_delivery > 60 and your_business and not your_business.get("has_delivery", False):
        recommendations.append(KPIRecommendation(
            metric="Delivery",
            current_value="Não oferece",
            benchmark_value=f"{pct_with_delivery:.0f}% dos concorrentes oferecem",
            recommendation="Implemente delivery via iFood/Rappi ou próprio. Essencial no mercado brasileiro atual.",
            priority="High",
            expected_impact="Expansão de 40-60% na base de clientes"
        ))
    
    # PIX recommendation
    if pct_accepts_pix > 70 and your_business and not your_business.get("accepts_pix", False):
        recommendations.append(KPIRecommendation(
            metric="Pagamento PIX",
            current_value="Não aceita",
            benchmark_value=f"{pct_accepts_pix:.0f}% dos concorrentes aceitam",
            recommendation="Implemente PIX imediatamente. É o método preferido de 70% dos brasileiros.",
            priority="High",
            expected_impact="Redução de perdas de venda por falta de opção de pagamento"
        ))
    
    # If no specific recommendations, give general ones
    if len(recommendations) == 0:
        recommendations.append(KPIRecommendation(
            metric="Manutenção de Liderança",
            current_value="Acima da média",
            benchmark_value="Continue assim",
            recommendation="Mantenha seus altos padrões e monitore a concorrência regularmente.",
            priority="Medium",
            expected_impact="Sustentabilidade de longo prazo"
        ))
    
    return recommendations


def generate_analytics(
    competitors: List[Competitor],
    radius_km: float,
    your_business: Optional[Dict] = None
) -> AnalyticsResponse:
    """Generate complete analytics and insights"""
    
    # Market density analysis
    market_density = analyze_market_density(competitors, radius_km)
    
    # Competitive positioning (if user data available)
    positioning = analyze_competitive_positioning(your_business, competitors)
    
    # Market share estimate
    market_share = estimate_market_share(your_business, competitors)
    
    # KPI recommendations
    kpis = generate_kpi_recommendations(your_business, competitors, market_density, positioning)
    
    # Generate summary
    summary_parts = [
        f"Encontramos {len(competitors)} concorrentes em um raio de {radius_km}km.",
        f"Densidade de mercado: {market_density.density_level} ({market_density.competitors_per_km2:.1f} concorrentes/km²).",
    ]
    
    if market_share:
        summary_parts.append(
            f"Estrutura de mercado: {market_share.market_structure}."
        )
    
    if positioning and positioning.percentile >= 50:
        summary_parts.append(
            f"Você está no top {100 - positioning.percentile:.0f}% em avaliações."
        )
    
    summary = " ".join(summary_parts)
    
    return AnalyticsResponse(
        market_density=market_density,
        competitive_positioning=positioning,
        market_share_estimate=market_share,
        kpi_recommendations=kpis,
        summary=summary
    )
