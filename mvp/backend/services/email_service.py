"""
Email service for sending analysis results to users
"""

import os
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Email configuration from environment
USE_MOCK_EMAIL = os.getenv("USE_MOCK_EMAIL", "true").lower() == "true"
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@competeintel.com.br")


def format_email_html(
    business_name: str,
    city: str,
    state: str,
    category: str,
    analysis_results: Dict[str, Any]
) -> str:
    """Format HTML email with analysis results"""
    
    analytics = analysis_results.get("analytics", {})
    competitors = analysis_results.get("competitors", [])
    total_found = analysis_results.get("total_found", 0)
    
    market_density = analytics.get("market_density", {})
    density_level = market_density.get("density_level", "N/A")
    total_competitors = market_density.get("total_competitors", 0)
    saturation_score = market_density.get("market_saturation_score", 0)
    
    kpi_recommendations = analytics.get("kpi_recommendations", [])
    
    # Build competitor list (top 5)
    competitor_list_html = ""
    for i, comp in enumerate(competitors[:5], 1):
        competitor_list_html += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #eee;">{i}</td>
            <td style="padding: 10px; border-bottom: 1px solid #eee;">{comp.get('name', 'N/A')}</td>
            <td style="padding: 10px; border-bottom: 1px solid #eee;">{comp.get('rating', 0):.1f} ⭐</td>
            <td style="padding: 10px; border-bottom: 1px solid #eee;">{comp.get('review_count', 0)} avaliações</td>
        </tr>
        """
    
    # Build KPI recommendations (top 3)
    kpi_html = ""
    for kpi in kpi_recommendations[:3]:
        priority_color = {
            "High": "#dc2626",
            "Medium": "#f59e0b",
            "Low": "#10b981"
        }.get(kpi.get("priority", "Medium"), "#6b7280")
        
        kpi_html += f"""
        <div style="margin-bottom: 20px; padding: 15px; background: #f9fafb; border-radius: 8px; border-left: 4px solid {priority_color};">
            <h3 style="margin: 0 0 10px 0; color: #1f2937; font-size: 16px;">{kpi.get('metric', 'N/A')}</h3>
            <p style="margin: 5px 0; color: #6b7280; font-size: 14px;">
                <strong>Atual:</strong> {kpi.get('current_value', 'N/A')} | 
                <strong>Benchmark:</strong> {kpi.get('benchmark_value', 'N/A')}
            </p>
            <p style="margin: 10px 0 0 0; color: #374151; font-size: 14px;">{kpi.get('recommendation', 'N/A')}</p>
        </div>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background-color: #f3f4f6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #059669 0%, #0284c7 100%); padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
                <h1 style="margin: 0; color: white; font-size: 28px;">📊 CompeteIntel</h1>
                <p style="margin: 10px 0 0 0; color: rgba(255,255,255,0.9); font-size: 16px;">Sua Análise Competitiva está pronta!</p>
            </div>
            
            <!-- Content -->
            <div style="background: white; padding: 30px; border-radius: 0 0 12px 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h2 style="margin: 0 0 20px 0; color: #1f2937; font-size: 22px;">Olá, {business_name}! 👋</h2>
                
                <p style="color: #4b5563; font-size: 15px; line-height: 1.6;">
                    Finalizamos a análise competitiva para <strong>{category}</strong> em <strong>{city}/{state}</strong>.
                    Aqui estão os principais insights:
                </p>
                
                <!-- Market Overview -->
                <div style="margin: 25px 0; padding: 20px; background: #f0fdf4; border-radius: 8px; border: 1px solid #bbf7d0;">
                    <h3 style="margin: 0 0 15px 0; color: #065f46; font-size: 18px;">📈 Visão Geral do Mercado</h3>
                    <div style="display: flex; gap: 20px; flex-wrap: wrap;">
                        <div style="flex: 1; min-width: 150px;">
                            <p style="margin: 0; color: #6b7280; font-size: 13px;">Total de Concorrentes</p>
                            <p style="margin: 5px 0 0 0; color: #1f2937; font-size: 24px; font-weight: bold;">{total_competitors}</p>
                        </div>
                        <div style="flex: 1; min-width: 150px;">
                            <p style="margin: 0; color: #6b7280; font-size: 13px;">Nível de Saturação</p>
                            <p style="margin: 5px 0 0 0; color: #1f2937; font-size: 24px; font-weight: bold;">{density_level}</p>
                        </div>
                        <div style="flex: 1; min-width: 150px;">
                            <p style="margin: 0; color: #6b7280; font-size: 13px;">Score de Saturação</p>
                            <p style="margin: 5px 0 0 0; color: #1f2937; font-size: 24px; font-weight: bold;">{saturation_score:.0f}/100</p>
                        </div>
                    </div>
                </div>
                
                <!-- Top Competitors -->
                <h3 style="margin: 30px 0 15px 0; color: #1f2937; font-size: 18px;">🏆 Top 5 Concorrentes</h3>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 25px;">
                    <thead>
                        <tr style="background: #f9fafb;">
                            <th style="padding: 10px; text-align: left; color: #6b7280; font-size: 13px; font-weight: 600;">#</th>
                            <th style="padding: 10px; text-align: left; color: #6b7280; font-size: 13px; font-weight: 600;">Nome</th>
                            <th style="padding: 10px; text-align: left; color: #6b7280; font-size: 13px; font-weight: 600;">Nota</th>
                            <th style="padding: 10px; text-align: left; color: #6b7280; font-size: 13px; font-weight: 600;">Avaliações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {competitor_list_html}
                    </tbody>
                </table>
                
                <!-- KPI Recommendations -->
                <h3 style="margin: 30px 0 15px 0; color: #1f2937; font-size: 18px;">💡 Recomendações Prioritárias</h3>
                {kpi_html}
                
                <!-- CTA -->
                <div style="margin: 30px 0; padding: 20px; background: #eff6ff; border-radius: 8px; text-align: center;">
                    <p style="margin: 0 0 15px 0; color: #1e40af; font-size: 15px;">
                        Quer análises contínuas e alertas em tempo real?
                    </p>
                    <a href="http://localhost:8080#pricing" style="display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #059669 0%, #0284c7 100%); color: white; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 15px;">
                        Ver Planos →
                    </a>
                </div>
                
                <!-- Footer -->
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center;">
                    <p style="margin: 0; color: #9ca3af; font-size: 13px;">
                        © 2024 CompeteIntel - Inteligência Competitiva para o Mercado Brasileiro
                    </p>
                    <p style="margin: 10px 0 0 0; color: #9ca3af; font-size: 12px;">
                        Esta análise foi gerada automaticamente com base em dados públicos.
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


def format_email_plaintext(
    business_name: str,
    city: str,
    state: str,
    category: str,
    analysis_results: Dict[str, Any]
) -> str:
    """Format plain text email with analysis results"""
    
    analytics = analysis_results.get("analytics", {})
    competitors = analysis_results.get("competitors", [])
    
    market_density = analytics.get("market_density", {})
    kpi_recommendations = analytics.get("kpi_recommendations", [])
    
    text = f"""
CompeteIntel - Análise Competitiva
=====================================

Olá, {business_name}!

Sua análise competitiva para {category} em {city}/{state} está pronta.

VISÃO GERAL DO MERCADO
----------------------
Total de Concorrentes: {market_density.get('total_competitors', 0)}
Nível de Saturação: {market_density.get('density_level', 'N/A')}
Score de Saturação: {market_density.get('market_saturation_score', 0):.0f}/100

TOP 5 CONCORRENTES
------------------
"""
    
    for i, comp in enumerate(competitors[:5], 1):
        text += f"{i}. {comp.get('name', 'N/A')} - {comp.get('rating', 0):.1f}⭐ ({comp.get('review_count', 0)} avaliações)\n"
    
    text += "\nRECOMENDAÇÕES PRIORITÁRIAS\n--------------------------\n"
    
    for kpi in kpi_recommendations[:3]:
        text += f"\n• {kpi.get('metric', 'N/A')}\n"
        text += f"  Atual: {kpi.get('current_value', 'N/A')} | Benchmark: {kpi.get('benchmark_value', 'N/A')}\n"
        text += f"  Recomendação: {kpi.get('recommendation', 'N/A')}\n"
    
    text += """
\n---
© 2024 CompeteIntel
Inteligência Competitiva para o Mercado Brasileiro
"""
    
    return text


async def send_analysis_email(
    to_email: str,
    business_name: str,
    city: str,
    state: str,
    category: str,
    analysis_results: Dict[str, Any]
) -> bool:
    """
    Send analysis results via email
    
    Args:
        to_email: Recipient email address
        business_name: Business name
        city: City name
        state: State abbreviation
        category: Business category
        analysis_results: Full analysis results from /api/search
    
    Returns:
        True if email sent successfully (or mocked), False otherwise
    """
    
    try:
        # Format email content
        html_content = format_email_html(business_name, city, state, category, analysis_results)
        text_content = format_email_plaintext(business_name, city, state, category, analysis_results)
        
        subject = f"📊 Análise Competitiva - {category} em {city}/{state}"
        
        if USE_MOCK_EMAIL:
            # Mock mode: just log the email
            logger.info("=" * 80)
            logger.info("MOCK EMAIL - Would send to: %s", to_email)
            logger.info("Subject: %s", subject)
            logger.info("=" * 80)
            logger.info("Plain text content preview:")
            logger.info(text_content[:500] + "..." if len(text_content) > 500 else text_content)
            logger.info("=" * 80)
            logger.info("HTML email prepared (length: %d chars)", len(html_content))
            logger.info("=" * 80)
            return True
        else:
            # Real email sending would go here
            # For now, this is a placeholder for future SMTP integration
            logger.warning("Real email sending not implemented yet. Set USE_MOCK_EMAIL=true")
            return False
            
    except Exception as e:
        logger.error("Error sending email: %s", str(e))
        return False
