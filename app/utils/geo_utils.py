"""
Utility functions for geocoding and distance calculations.
"""
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import logging
from functools import lru_cache

# Configure logger
logger = logging.getLogger(__name__)

# Initialize geocoder
geolocator = Nominatim(user_agent="clinic_finder_app")


@lru_cache(maxsize=128)
def geocode_address(address: str):
    """
    Convert address to geographical coordinates (latitude, longitude).
    
    Args:
        address: String representation of an address
        
    Returns:
        Tuple of (latitude, longitude) or None if geocoding fails
    """
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        return None
    except Exception as e:
        logger.error(f"Error geocoding address {address}: {str(e)}")
        return None


def calculate_distance(address1: str, address2: str):
    """
    Calculate the distance between two addresses in kilometers.
    
    Args:
        address1: First address
        address2: Second address
        
    Returns:
        Distance in kilometers or None if geocoding fails
    """
    coords1 = geocode_address(address1)
    coords2 = geocode_address(address2)
    
    if coords1 and coords2:
        distance = geodesic(coords1, coords2).kilometers
        return round(distance, 2)
    return None
