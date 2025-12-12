"""
Mock competitor data for Brazilian businesses across major cities
"""

from typing import List, Dict
import random

# Major Brazilian cities with coordinates
CITIES = {
    "São Paulo": {"lat": -23.5505, "lng": -46.6333, "state": "SP"},
    "Rio de Janeiro": {"lat": -22.9068, "lng": -43.1729, "state": "RJ"},
    "Belo Horizonte": {"lat": -19.9167, "lng": -43.9345, "state": "MG"},
    "Brasília": {"lat": -15.7939, "lng": -47.8828, "state": "DF"},
    "Curitiba": {"lat": -25.4284, "lng": -49.2733, "state": "PR"},
    "Porto Alegre": {"lat": -30.0346, "lng": -51.2177, "state": "RS"},
    "Salvador": {"lat": -12.9714, "lng": -38.5014, "state": "BA"},
    "Fortaleza": {"lat": -3.7172, "lng": -38.5434, "state": "CE"},
    "Recife": {"lat": -8.0476, "lng": -34.8770, "state": "PE"},
    "Manaus": {"lat": -3.1190, "lng": -60.0217, "state": "AM"},
}

# Business categories with CNAE codes
BUSINESS_CATEGORIES = {
    "Padaria": {
        "cnae": "4721-1/02",
        "description": "Padaria e confeitaria com predominância de produção própria",
        "names": [
            "Padaria {} Pães", "Padaria e Confeitaria {}", "Pão Quente {}",
            "{} Padaria Artesanal", "Delícias da {}", "Padaria Tradicional {}",
            "Casa do Pão {}", "{} Bakery", "Sabor e Arte {}"
        ]
    },
    "Restaurante": {
        "cnae": "5611-2/01",
        "description": "Restaurantes e similares",
        "names": [
            "Restaurante {}", "Sabor da {}", "{} Gourmet", "Cozinha {}",
            "Tempero {}", "Delícias {}", "{} Food", "Bistrô {}",
            "Cantina {}", "{} Mesa"
        ]
    },
    "Farmácia": {
        "cnae": "4771-7/01",
        "description": "Comércio varejista de produtos farmacêuticos",
        "names": [
            "Farmácia {}", "Drogaria {}", "{} Farma", "Farmácia Popular {}",
            "{} Saúde", "Bem Estar {}", "Farmácia São {}", "{} Medicamentos"
        ]
    },
    "Supermercado": {
        "cnae": "4711-3/02",
        "description": "Supermercado",
        "names": [
            "Supermercado {}", "Super {}", "{} Alimentos", "Mercado {}",
            "{} Super", "Empório {}", "Mini Mercado {}", "{} Market"
        ]
    },
    "Cafeteria": {
        "cnae": "5611-2/04",
        "description": "Bares e outros estabelecimentos especializados em servir bebidas",
        "names": [
            "Café {}", "Cafeteria {}", "{} Coffee", "Coffee {}",
            "Aroma de {}", "{} Espresso", "Café Especial {}", "{} Café"
        ]
    },
    "Academia": {
        "cnae": "9313-1/00",
        "description": "Atividades de condicionamento físico",
        "names": [
            "Academia {}", "Fitness {}", "{} Gym", "Shape {}",
            "Corpo e Mente {}", "{} Fitness", "Esporte {}", "{} Training"
        ]
    },
    "Pet Shop": {
        "cnae": "4789-0/05",
        "description": "Comércio varejista de animais vivos e de artigos e alimentos para animais de estimação",
        "names": [
            "Pet Shop {}", "Mundo Pet {}", "{} Pets", "Bicho {}",
            "{} Pet Store", "Amigo Animal {}", "Pet {}", "{} Vet Shop"
        ]
    },
    "Lanchonete": {
        "cnae": "5611-2/03",
        "description": "Lanchonetes, casas de chá, de sucos e similares",
        "names": [
            "Lanchonete {}", "Lanches {}", "{} Burger", "Snack {}",
            "{} Lanches", "Quick {}", "Fast {}", "{} Express"
        ]
    }
}

# Street name prefixes for realistic addresses
STREET_PREFIXES = ["Rua", "Avenida", "Travessa", "Alameda", "Praça"]
STREET_NAMES = [
    "das Flores", "do Comércio", "Central", "Principal", "Paulista",
    "Getúlio Vargas", "Santos Dumont", "Dom Pedro", "XV de Novembro",
    "Sete de Setembro", "da Independência", "Rio Branco", "Tiradentes",
    "São João", "da República", "do Mercado", "das Palmeiras"
]

# Social media presence templates
SOCIAL_MEDIA = {
    "high": {
        "has_instagram": True,
        "has_facebook": True,
        "has_website": True,
        "instagram_followers": random.randint(5000, 50000),
        "facebook_likes": random.randint(3000, 30000)
    },
    "medium": {
        "has_instagram": True,
        "has_facebook": True,
        "has_website": False,
        "instagram_followers": random.randint(500, 5000),
        "facebook_likes": random.randint(300, 3000)
    },
    "low": {
        "has_instagram": False,
        "has_facebook": True,
        "has_website": False,
        "instagram_followers": 0,
        "facebook_likes": random.randint(50, 500)
    }
}


def generate_cnpj() -> str:
    """Generate a fake but formatted CNPJ"""
    digits = [random.randint(0, 9) for _ in range(14)]
    return f"{digits[0]}{digits[1]}.{digits[2]}{digits[3]}{digits[4]}.{digits[5]}{digits[6]}{digits[7]}/{digits[8]}{digits[9]}{digits[10]}{digits[11]}-{digits[12]}{digits[13]}"


def generate_phone() -> str:
    """Generate a Brazilian phone number"""
    ddd = random.choice([11, 21, 31, 41, 51, 61, 71, 81, 85, 92])  # Major city area codes
    first_digit = 9  # Mobile
    rest = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return f"({ddd}) {first_digit}{rest[:4]}-{rest[4:]}"


def generate_address(city: str, state: str) -> Dict[str, str]:
    """Generate a realistic Brazilian address"""
    prefix = random.choice(STREET_PREFIXES)
    name = random.choice(STREET_NAMES)
    number = random.randint(1, 999)
    neighborhood = random.choice(["Centro", "Vila Nova", "Jardim das Flores", "Bairro Alto", "Zona Sul"])
    cep_base = random.randint(10000, 99999)
    cep = f"{cep_base:05d}-{random.randint(100, 999)}"
    
    return {
        "street": f"{prefix} {name}, {number}",
        "neighborhood": neighborhood,
        "city": city,
        "state": state,
        "postal_code": cep,
        "country": "Brasil"
    }


def add_random_offset(lat: float, lng: float, max_km: float = 5.0) -> tuple:
    """Add random offset to coordinates (approximately in km)"""
    # Rough conversion: 1 degree ≈ 111 km
    km_to_deg = 1 / 111.0
    
    offset_lat = random.uniform(-max_km * km_to_deg, max_km * km_to_deg)
    offset_lng = random.uniform(-max_km * km_to_deg, max_km * km_to_deg)
    
    return (round(lat + offset_lat, 6), round(lng + offset_lng, 6))


def generate_mock_competitors(
    city: str,
    category: str,
    count: int = 10,
    radius_km: float = 5.0
) -> List[Dict]:
    """
    Generate mock competitor data for a specific city and business category
    
    Args:
        city: City name (must be in CITIES dict)
        category: Business category (must be in BUSINESS_CATEGORIES dict)
        count: Number of competitors to generate
        radius_km: Maximum distance from city center in km
    
    Returns:
        List of competitor dictionaries
    """
    if city not in CITIES:
        raise ValueError(f"Unknown city: {city}")
    if category not in BUSINESS_CATEGORIES:
        raise ValueError(f"Unknown category: {category}")
    
    city_data = CITIES[city]
    category_data = BUSINESS_CATEGORIES[category]
    competitors = []
    
    for i in range(count):
        # Generate random coordinates within radius
        lat, lng = add_random_offset(city_data["lat"], city_data["lng"], radius_km)
        
        # Generate business name
        name_template = random.choice(category_data["names"])
        location_name = random.choice(["Central", "Norte", "Sul", "Leste", "Oeste", city])
        business_name = name_template.format(location_name)
        
        # Random rating and reviews
        rating = round(random.uniform(3.5, 5.0), 1)
        review_count = random.randint(10, 500)
        
        # Social media presence (more established businesses have better presence)
        if rating >= 4.5 and review_count > 200:
            social_tier = "high"
        elif rating >= 4.0 and review_count > 100:
            social_tier = "medium"
        else:
            social_tier = "low"
        
        social_data = SOCIAL_MEDIA[social_tier].copy()
        social_data["instagram_followers"] = random.randint(
            *{"high": (5000, 50000), "medium": (500, 5000), "low": (0, 500)}[social_tier]
        )
        
        # Estimate revenue based on various factors
        # This is a simplified model - in reality would be much more complex
        base_revenue = {
            "Padaria": 30000,
            "Restaurante": 50000,
            "Farmácia": 80000,
            "Supermercado": 150000,
            "Cafeteria": 25000,
            "Academia": 40000,
            "Pet Shop": 35000,
            "Lanchonete": 20000
        }.get(category, 30000)
        
        # Multiply by rating factor, review factor, and add randomness
        revenue_factor = (rating / 5.0) * (1 + review_count / 1000) * random.uniform(0.7, 1.5)
        estimated_monthly_revenue = int(base_revenue * revenue_factor)
        
        competitor = {
            "id": f"mock_{category.lower()}_{city.lower().replace(' ', '_')}_{i+1}",
            "name": business_name,
            "category": category,
            "cnae_code": category_data["cnae"],
            "cnae_description": category_data["description"],
            "cnpj": generate_cnpj(),
            "coordinates": {
                "latitude": lat,
                "longitude": lng
            },
            "address": generate_address(city, city_data["state"]),
            "phone": generate_phone(),
            "rating": rating,
            "review_count": review_count,
            "online_presence": social_data,
            "is_verified": random.choice([True, True, True, False]),  # 75% verified
            "opening_year": random.randint(2010, 2024),
            "employee_count_estimate": random.choice([
                "1-5", "1-5", "6-10", "6-10", "11-25", "26-50", "50+"
            ]),
            "estimated_monthly_revenue": estimated_monthly_revenue,
            "has_delivery": random.choice([True, False]),
            "accepts_pix": random.choice([True, True, True, False]),  # 75% accept PIX
            "accepts_cards": random.choice([True, True, True, True, False]),  # 80% accept cards
        }
        
        competitors.append(competitor)
    
    # Sort by rating descending
    competitors.sort(key=lambda x: x["rating"], reverse=True)
    
    return competitors


# Pre-generated datasets for quick access
MOCK_DATA_CACHE = {}

def get_mock_competitors(city: str, category: str, count: int = 10) -> List[Dict]:
    """Get mock competitors with caching"""
    cache_key = f"{city}_{category}_{count}"
    
    if cache_key not in MOCK_DATA_CACHE:
        MOCK_DATA_CACHE[cache_key] = generate_mock_competitors(city, category, count)
    
    return MOCK_DATA_CACHE[cache_key]
