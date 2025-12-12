"""
CNPJ validation and lookup service
Currently uses mock validation, ready for real API integration
"""

import re
from typing import Optional, Dict


def validate_cnpj(cnpj: str) -> bool:
    """
    Validate CNPJ format and check digit
    
    Args:
        cnpj: CNPJ string (with or without formatting)
    
    Returns:
        True if valid, False otherwise
    """
    # Remove formatting
    cnpj_clean = re.sub(r'[^\d]', '', cnpj)
    
    # Check length
    if len(cnpj_clean) != 14:
        return False
    
    # Check if all digits are the same (invalid)
    if len(set(cnpj_clean)) == 1:
        return False
    
    # Validate check digits
    def calculate_digit(cnpj_partial: str, weights: list) -> int:
        total = sum(int(digit) * weight for digit, weight in zip(cnpj_partial, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    # First check digit
    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    digit1 = calculate_digit(cnpj_clean[:12], weights1)
    
    if int(cnpj_clean[12]) != digit1:
        return False
    
    # Second check digit
    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    digit2 = calculate_digit(cnpj_clean[:13], weights2)
    
    if int(cnpj_clean[13]) != digit2:
        return False
    
    return True


def format_cnpj(cnpj: str) -> str:
    """
    Format CNPJ to standard format: XX.XXX.XXX/XXXX-XX
    
    Args:
        cnpj: CNPJ string (with or without formatting)
    
    Returns:
        Formatted CNPJ string
    """
    # Remove formatting
    cnpj_clean = re.sub(r'[^\d]', '', cnpj)
    
    if len(cnpj_clean) != 14:
        raise ValueError("CNPJ must have 14 digits")
    
    return f"{cnpj_clean[:2]}.{cnpj_clean[2:5]}.{cnpj_clean[5:8]}/{cnpj_clean[8:12]}-{cnpj_clean[12:14]}"


def lookup_cnpj(cnpj: str) -> Optional[Dict]:
    """
    Look up CNPJ information
    
    Currently returns mock data. In production, would integrate with:
    - Receita Federal API (free, limited)
    - Commercial CNPJ APIs (Brasil API, ReceitaWS, etc.)
    
    Args:
        cnpj: CNPJ string
    
    Returns:
        Company information dict or None if not found
    
    TODO: Implement real API integration
    """
    if not validate_cnpj(cnpj):
        return None
    
    # Mock response
    # In production, would call external API
    """
    Example real implementation:
    
    import requests
    
    # Using ReceitaWS (free, rate-limited)
    cnpj_clean = re.sub(r'[^\d]', '', cnpj)
    response = requests.get(f'https://www.receitaws.com.br/v1/cnpj/{cnpj_clean}')
    
    if response.status_code == 200:
        data = response.json()
        return {
            'cnpj': data.get('cnpj'),
            'name': data.get('nome'),
            'trade_name': data.get('fantasia'),
            'status': data.get('situacao'),
            'opening_date': data.get('abertura'),
            'legal_nature': data.get('natureza_juridica'),
            'main_activity': data.get('atividade_principal', [{}])[0],
            'address': {
                'street': data.get('logradouro'),
                'number': data.get('numero'),
                'neighborhood': data.get('bairro'),
                'city': data.get('municipio'),
                'state': data.get('uf'),
                'postal_code': data.get('cep')
            },
            'phone': data.get('telefone'),
            'email': data.get('email')
        }
    
    return None
    """
    
    # Mock return
    return {
        'cnpj': format_cnpj(cnpj),
        'name': "Empresa Exemplo Ltda",
        'trade_name': "Exemplo",
        'status': "ATIVA",
        'opening_date': "01/01/2020",
        'legal_nature': "Sociedade Empresária Limitada",
        'main_activity': {
            'code': '47.21-1/02',
            'description': 'Padaria e confeitaria com predominância de produção própria'
        }
    }


def get_cnae_description(cnae_code: str) -> str:
    """
    Get description for a CNAE code
    
    Args:
        cnae_code: CNAE code (e.g., "4721-1/02")
    
    Returns:
        Description of the activity
    """
    # Common CNAE codes for Brazilian businesses
    cnae_map = {
        "4721-1/02": "Padaria e confeitaria com predominância de produção própria",
        "5611-2/01": "Restaurantes e similares",
        "5611-2/03": "Lanchonetes, casas de chá, de sucos e similares",
        "5611-2/04": "Bares e outros estabelecimentos especializados em servir bebidas",
        "4771-7/01": "Comércio varejista de produtos farmacêuticos sem manipulação de fórmulas",
        "4711-3/02": "Supermercado",
        "4712-1/00": "Comércio varejista de mercadorias em geral, com predominância de produtos alimentícios - minimercados, mercearias e armazéns",
        "9313-1/00": "Atividades de condicionamento físico",
        "4789-0/05": "Comércio varejista de animais vivos e de artigos e alimentos para animais de estimação",
        "4721-1/03": "Comércio varejista de laticínios e frios",
        "4722-9/01": "Comércio varejista de carnes - açougues",
    }
    
    return cnae_map.get(cnae_code, "Atividade não classificada")
