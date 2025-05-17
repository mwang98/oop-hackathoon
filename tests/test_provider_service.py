"""
Tests for provider service functions.
"""
import pytest
import asyncio
import os
from unittest.mock import patch, MagicMock
from app.services.provider_service import get_location_from_zip, map_symptoms_to_specialties, load_specialties
from app.models.schemas import Location, ProviderSpecialty


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


@pytest.mark.asyncio
async def test_load_specialties():
    """Test loading of specialties list."""
    specialties = load_specialties()
    
    # Check that we got a list of specialties
    assert isinstance(specialties, list)
    assert len(specialties) > 0
    
    # Check that each item is a ProviderSpecialty
    for specialty in specialties:
        assert isinstance(specialty, ProviderSpecialty)
        assert specialty.id
        assert specialty.name


@pytest.mark.asyncio
@patch('openai.OpenAI')
async def test_map_symptoms_to_specialties(mock_openai):
    """Test mapping symptoms to specialties using mocked LLM."""
    # Set up the mock for OpenAI
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Cardiology, Neurology"
    
    mock_client.chat.completions.create.return_value = mock_response
    
    # Mock environment variable
    os.environ["OPENAI_API_KEY"] = "mock-api-key"
    
    # Test with a list of symptoms
    symptoms = ["chest pain", "shortness of breath", "dizziness"]
    
    # Call the function
    specialties = await map_symptoms_to_specialties(symptoms)
    
    # Check that the OpenAI API was called
    mock_client.chat.completions.create.assert_called_once()
    
    # Check that we got a list of specialties back
    assert isinstance(specialties, list)
    
    # We can't assert exact specialties as they're dependent on the mock,
    # but we can check the structure
    for specialty in specialties:
        assert isinstance(specialty, ProviderSpecialty)


if __name__ == "__main__":
    asyncio.run(test_get_location_from_zip_valid())
    # Skip the other tests when running directly