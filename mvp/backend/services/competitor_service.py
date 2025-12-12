"""
Competitor discovery service
Currently uses mock data, ready for Google Places API integration
"""

from typing import List, Optional
from models.schemas import Competitor, Coordinates, Address, OnlinePresence
from data.mock_competitors import get_mock_competitors, CITIES, BUSINESS_CATEGORIES
from services.analysis_service import calculate_distance
import os


USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "true").lower() == "true"


def search_competitors(
    category: str,
    city: str,
    coordinates: Optional[Coordinates] = None,
    radius_km: float = 5.0,
    max_results: int = 10,
    neighborhood: Optional[str] = None,
    cep: Optional[str] = None
) -> List[Competitor]:
    """
    Search for competitors in a given city and category
    
    Args:
        category: Business category (e.g., "Padaria")
        city: City name (e.g., "São Paulo")
        coordinates: Optional coordinates for distance calculations
        radius_km: Search radius in kilometers
        max_results: Maximum number of results to return
        neighborhood: Optional neighborhood filter
        cep: Optional CEP (postal code) filter
    
    Returns:
        List of Competitor objects
    """
    
    if USE_MOCK_DATA:
        return _search_competitors_mock(category, city, coordinates, radius_km, max_results, neighborhood, cep)
    else:
        # TODO: Implement Google Places API integration
        return _search_competitors_google_places(category, city, coordinates, radius_km, max_results)


def _search_competitors_mock(
    category: str,
    city: str,
    coordinates: Optional[Coordinates],
    radius_km: float,
    max_results: int,
    neighborhood: Optional[str] = None,
    cep: Optional[str] = None
) -> List[Competitor]:
    """Search using mock data"""
    
    # Normalize city name for lookup
    city_normalized = city.strip()
    
    # Find closest matching city
    if city_normalized not in CITIES:
        # Try to find a close match
        for city_key in CITIES.keys():
            if city_key.lower() in city_normalized.lower() or city_normalized.lower() in city_key.lower():
                city_normalized = city_key
                break
        else:
            # Default to São Paulo if no match
            city_normalized = "São Paulo"
    
    # Normalize category
    category_normalized = category.strip()
    if category_normalized not in BUSINESS_CATEGORIES:
        # Try to find close match
        for cat_key in BUSINESS_CATEGORIES.keys():
            if cat_key.lower() in category_normalized.lower() or category_normalized.lower() in cat_key.lower():
                category_normalized = cat_key
                break
        else:
            # Default to Padaria if no match
            category_normalized = "Padaria"
    
    # Get mock data (request more to allow for filtering)
    mock_data = get_mock_competitors(city_normalized, category_normalized, count=max_results * 3)
    
    # Use provided coordinates or city center
    if coordinates:
        ref_lat = coordinates.latitude
        ref_lng = coordinates.longitude
    else:
        city_data = CITIES[city_normalized]
        ref_lat = city_data["lat"]
        ref_lng = city_data["lng"]
    
    competitors = []
    
    for data in mock_data:
        # Calculate distance from reference point
        distance = calculate_distance(
            ref_lat,
            ref_lng,
            data["coordinates"]["latitude"],
            data["coordinates"]["longitude"]
        )
        
        # Only include if within radius
        if distance > radius_km:
            continue
        
        # Filter by neighborhood if provided
        if neighborhood:
            if neighborhood.lower() not in data["address"]["neighborhood"].lower():
                continue
        
        # Filter by CEP if provided (match first 5 digits for area match)
        if cep:
            # Remove formatting from CEP
            cep_clean = cep.replace("-", "").replace(".", "")
            data_cep_clean = data["address"]["postal_code"].replace("-", "").replace(".", "")
            # Match first 5 digits (same area)
            if not data_cep_clean.startswith(cep_clean[:5]):
                continue
        
        competitor = Competitor(
            id=data["id"],
            name=data["name"],
            category=data["category"],
            cnae_code=data["cnae_code"],
            cnae_description=data["cnae_description"],
            cnpj=data["cnpj"],
            coordinates=Coordinates(**data["coordinates"]),
            address=Address(**data["address"]),
            phone=data["phone"],
            rating=data["rating"],
            review_count=data["review_count"],
            distance_km=round(distance, 2),
            online_presence=OnlinePresence(**data["online_presence"]),
            is_verified=data["is_verified"],
            opening_year=data["opening_year"],
            employee_count_estimate=data["employee_count_estimate"],
            estimated_monthly_revenue=data["estimated_monthly_revenue"],
            has_delivery=data["has_delivery"],
            accepts_pix=data["accepts_pix"],
            accepts_cards=data["accepts_cards"]
        )
        competitors.append(competitor)
        
        # Stop if we have enough results
        if len(competitors) >= max_results:
            break
    
    # Sort by distance
    competitors.sort(key=lambda x: x.distance_km if x.distance_km else 999)
    
    return competitors[:max_results]


def _search_competitors_google_places(
    category: str,
    city: str,
    coordinates: Optional[Coordinates],
    radius_km: float,
    max_results: int
) -> List[Competitor]:
    """
    Search using Google Places API
    
    TODO: Implement when ready to integrate real API
    
    Implementation steps:
    1. Use googlemaps Python client
    2. Search for places matching category within radius
    3. Fetch place details for each result
    4. Enrich with additional data sources (social media, CNPJ, etc.)
    5. Build Competitor objects from combined data
    
    Example code structure:
    ```python
    import googlemaps
    
    gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
    
    # Nearby search
    places = gmaps.places_nearby(
        location=(coordinates.latitude, coordinates.longitude),
        radius=radius_km * 1000,  # Convert to meters
        keyword=category,
        language='pt-BR'
    )
    
    competitors = []
    for place in places['results'][:max_results]:
        # Get detailed info
        details = gmaps.place(place['place_id'], language='pt-BR')
        
        # Build Competitor object from details
        # Enrich with CNPJ data, social media, etc.
        competitor = build_competitor_from_place(details)
        competitors.append(competitor)
    
    return competitors
    ```
    """
    raise NotImplementedError(
        "Google Places API integration not yet implemented. "
        "Set USE_MOCK_DATA=true to use mock data."
    )


def build_competitor_from_place(place_details: dict) -> Competitor:
    """
    Build a Competitor object from Google Places API data
    
    TODO: Implement when integrating real API
    """
    pass
