"""
Schema definitions for provider finder application.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class Location(BaseModel):
    """Location information with latitude and longitude."""
    latitude: float
    longitude: float


class ProviderSpecialty(BaseModel):
    """Provider specialty information."""
    id: str
    name: str
    description: Optional[str] = None


class ProviderInfo(BaseModel):
    """Provider information."""
    id: str
    name: str
    specialties: List[ProviderSpecialty]
    address: str
    zip_code: str
    location: Location
    distance: Optional[float] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[float] = None
    availability: Optional[Dict] = None


class ProviderConfirmationInfo(BaseModel):
    """Provider confirmation information after connecting."""
    provider_id: str
    provider_name: str
    confirmation_code: str
    status: str
    contact_info: Dict
    additional_info: Optional[Dict] = None
