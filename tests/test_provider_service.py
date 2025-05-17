"""
Tests for provider service functions.
"""
import pytest
import asyncio
from app.services.provider_service import get_location_from_zip
from app.models.schemas import Location


@pytest.mark.asyncio
async def test_get_location_from_zip_valid():
    """Test the conversion of a valid zip code to lat/long coordinates."""
    # Test with a known zip code (San Francisco)
    zip_code = "94105"
    
    # Call the function
    location = await get_location_from_zip(zip_code)
    
    # Assert that we got a Location object
    assert isinstance(location, Location)
    
    # Assert that latitude and longitude are reasonable values
    assert 37.0 < location.latitude < 38.0  # San Francisco area
    assert -123.0 < location.longitude < -122.0  # San Francisco area
    
    # Test with more precise expected values (these may need adjustment based on actual values)
    assert abs(location.latitude - 37.789) < 0.1
    assert abs(location.longitude - (-122.39)) < 0.1


if __name__ == "__main__":
    asyncio.run(test_get_location_from_zip_valid())