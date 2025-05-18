"""
Provider finder service functions.
"""

from typing import List, Dict, Optional, Tuple
import pgeocode
import json
import logging
from app.models.schemas import (
    Location,
    ProviderInfo,
    ProviderConfirmationInfo,
    ProviderRecommendations
)
from app.utils.prompt import PromptGenerator
from app.utils.llm_client import LLMClient, process_json_response
import requests

prompt_generator = PromptGenerator('app/data/specialties.json')
llm_client = LLMClient(api_key="api_key_here")  # Replace with your actual API key
logger = logging.getLogger("provider_finder.service")


async def get_location_from_zip(zip_code: str) -> Location:
    """
    Convert zip code to latitude and longitude coordinates.

    Args:
        zip_code: The zip code to convert

    Returns:
        Location with latitude and longitude
    """
    try:
        # Create a US geocoder (assuming US zip codes)
        nomi = pgeocode.Nominatim("us")

        # Query the geocoder with the zip code
        result = nomi.query_postal_code(zip_code)

        # Extract latitude and longitude
        latitude = float(result.latitude)
        longitude = float(result.longitude)

        # Return a Location object with the coordinates
        return Location(latitude=latitude, longitude=longitude)
    except Exception as e:
        # Handle errors (invalid zip code, service unavailable, etc.)
        print(f"Error converting zip code to coordinates: {e}")
        # Return a default location (or raise an exception depending on requirements)
        raise ValueError(f"Could not determine location for zip code: {zip_code}")


async def get_providers_by_location(
    location: Location, radius: float = 25.0
) -> List[ProviderInfo]:
    """
    Find providers within a specific radius of a location.

    Args:
        location: The location (lat/long) to search around
        radius: Search radius in kilometers

    Returns:
        List of providers in the area
    """
    logger.info(f"Searching for providers at coordinates: {location.latitude}, {location.longitude}, radius: {radius} km")
    
    res = requests.post(
        "https://www.medicare.gov/api/care-compare/provider",
        json={
            "type": "Physician",
            "filters": {
                "radiusSearch": {
                    "coordinates": {
                        "lon": location.longitude,
                        "lat": location.latitude,
                    },
                    "radius": radius,
                }
            },
            "returnAllResults": True,
            "sort": ["closest"],
        },
    )
    # Log response information more thoroughly
    logger.info(f"API Response Status: {res.status_code}")
    return convert_raw_response_to_provider_info(res.json())

def convert_raw_response_to_provider_info(raw_response: dict) -> List[ProviderInfo]:
    """
    Convert raw response to provider info.
    """
    return [ProviderInfo(**provider) for provider in raw_response["results"]]

async def map_symptoms_to_specialties(symptom_description: str) -> List[Tuple[str, str, str]]:
    """
    Map patient symptoms to relevant provider specialties.

    Args:
        symptom_description: The description of the patient's symptoms

    Returns:
        List of provider specialties that can address the symptoms
    """
    prompt = prompt_generator.create_specialty_matching_prompt(symptom_description)
    response = llm_client.make_chat_completions_request(
        model="27b-text-it",
        messages=[
            {"role": "system", "content": "You are a medical professional helping to match patients to the correct medical specialty based on their symptoms and conditions. Always respond with properly structured JSON as instructed."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,  # Lower temperature for more focused/predictable responses
        max_tokens=300,
    )
    processed_response = process_json_response(response)
    return [
        (item.get("RECOMMENDED_SPECIALTY", ""), item.get("REASONING", ""), item.get("CONFIDENCE", "Low"))
        for item in processed_response
    ]

async def recommend_providers(
    zip_code: str, symptom_description: str, radius: float = 25.0
) -> List[ProviderRecommendations]:
    """
    Recommend providers based on location and optionally symptoms.

    Args:
        zip_code: Patient's zip code
        symptom_description: Description of patient's symptoms 
        radius: Search radius in kilometers

    Returns:
        List of recommended providers
    """
    logger.info(f"Finding providers for zip code: {zip_code} with radius: {radius} km")

    # Get location from zip code
    location = await get_location_from_zip(zip_code)
    logger.info(f"Location coordinates: {location.latitude}, {location.longitude}")

    # Get providers in the area
    providers = await get_providers_by_location(location, radius)
    logger.info(f"Found {len(providers)} providers in the area.")

    # Construct a list of (set(specialty), provider) tuples
    provider_specialty_list = [
        (set(s.specialty_name for s in provider.physician.specialties), provider) for provider in providers
    ]

    provider_recommendations = []
    
    # If symptoms provided, filter by appropriate specialties
    if symptom_description:
        result_list = await map_symptoms_to_specialties(symptom_description)

        for specialty, reasoning, confidence in result_list:
            selected_providers = _get_providers_by_specialty(specialty, provider_specialty_list)
            recommendation = ProviderRecommendations(
                provider_infos=selected_providers,
                reasoning=reasoning,
                confidence=confidence,
            )
            provider_recommendations.append(recommendation)
            logger.info(f"Recommended specialty: {specialty} with reasoning: {reasoning}, confidence: {confidence}")
            logger.info(f"Found {len(selected_providers)} providers for specialty: {specialty}")

    return provider_recommendations

async def connect_providers(
    selected_providers: List[ProviderInfo],
) -> List[ProviderConfirmationInfo]:
    """
    Initiate connection with selected providers.

    Args:
        selected_providers: List of providers selected by the patient

    Returns:
        List of provider confirmations with contact details
    """
    # TODO: Implement provider connection logic
    # This might involve sending notifications to providers, creating records in a database, etc.

    confirmations = []
    for provider in selected_providers:
        # Create a confirmation for each provider
        confirmation = ProviderConfirmationInfo(
            provider_id=provider.id,
            provider_name=provider.name,
            confirmation_code="",  # Generate a unique code
            status="pending",
            contact_info={
                "phone": provider.phone,
                "email": "provider@example.com",  # This would come from the provider data
            },
        )
        confirmations.append(confirmation)

    return confirmations


def _get_providers_by_specialty(
        specialty: str,
        provider_specialty_list: List[Tuple[set[str], ProviderInfo]],
) -> List[ProviderInfo]:
    return [
        provider
        for specialty_set, provider in provider_specialty_list
        if specialty in specialty_set
    ]