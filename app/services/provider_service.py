"""
Provider finder service functions.
"""
from typing import List, Dict, Optional
import json
import os
import pgeocode
import openai
from app.models.schemas import Location, ProviderInfo, ProviderSpecialty, ProviderConfirmationInfo


# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def load_specialties() -> List[ProviderSpecialty]:
    """
    Load the list of available provider specialties.
    
    Returns:
        List of ProviderSpecialty objects
    """
    # Check for specialties file in project directory first, then in Downloads
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "specialties.json"),
        os.path.expanduser("~/Downloads/specialties.json")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                specialties_data = json.load(f)
                
            return [
                ProviderSpecialty(
                    id=specialty["id"],
                    name=specialty["specialtyName"],
                    description=specialty.get("description", None)
                )
                for specialty in specialties_data
            ]
    
    # If no file found, return a default set of common specialties
    # This is a fallback option and should be replaced with a proper database or file
    return [
        ProviderSpecialty(id="1", name="General Practice", description="Primary care for general health issues"),
        ProviderSpecialty(id="2", name="Cardiology", description="Heart and cardiovascular system"),
        ProviderSpecialty(id="3", name="Dermatology", description="Skin conditions"),
        ProviderSpecialty(id="4", name="Orthopedics", description="Musculoskeletal system and injuries"),
        ProviderSpecialty(id="5", name="Neurology", description="Brain and nervous system conditions")
    ]


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
        nomi = pgeocode.Nominatim('us')
        
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


async def get_providers_by_location(location: Location, radius: float = 25.0) -> List[ProviderInfo]:
    """
    Find providers within a specific radius of a location.
    
    Args:
        location: The location (lat/long) to search around
        radius: Search radius in kilometers
        
    Returns:
        List of providers in the area
    """
    # TODO: Implement provider search by location and radius
    # This could query a database or external API
    pass


async def map_symptoms_to_specialties(symptoms: List[str]) -> List[ProviderSpecialty]:
    """
    Map patient symptoms to relevant provider specialties using LLM.
    
    Args:
        symptoms: List of patient symptoms
        
    Returns:
        List of provider specialties that can address the symptoms
    """
    if not symptoms:
        return []
    
    # Load available specialties
    available_specialties = load_specialties()
    
    # Prepare specialty information for the LLM prompt
    specialty_info = "\n".join([
        f"- {specialty.name}: {specialty.description or 'No description available'}"
        for specialty in available_specialties
    ])
    
    # Combine symptoms into a single description
    symptom_description = ", ".join(symptoms)
    
    # Create a prompt for the LLM
    prompt = f"""
    Given the following patient symptoms:
    "{symptom_description}"
    
    And these available medical specialties:
    {specialty_info}
    
    Identify the most relevant medical specialties that would be appropriate for treating these symptoms.
    Return only the names of the specialties, separated by commas. Match to multiple specialties if appropriate.
    """
    
    try:
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found in environment variables")
        
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical specialty matching assistant. Your job is to match patient symptoms to appropriate medical specialties. Be precise and thorough."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Low temperature for more deterministic responses
            max_tokens=150
        )
        
        # Extract specialty names from the response
        specialty_names = [name.strip() for name in response.choices[0].message.content.split(",")]
        
        # Match the specialty names to our available specialties
        matched_specialties = [
            specialty for specialty in available_specialties
            if any(specialty.name.lower() == name.lower() for name in specialty_names)
        ]
        
        # If no matches found, return a default (General Practice)
        if not matched_specialties:
            # Find general practice or primary care in our available specialties
            default_specialties = [
                specialty for specialty in available_specialties
                if any(term in specialty.name.lower() for term in ["general", "primary", "family"])
            ]
            if default_specialties:
                matched_specialties = default_specialties[:1]  # Just take the first one
        
        return matched_specialties
        
    except Exception as e:
        print(f"Error in LLM symptom mapping: {e}")
        # Fallback: return general practice or first specialty as default
        fallback_specialties = [
            specialty for specialty in available_specialties
            if any(term in specialty.name.lower() for term in ["general", "primary", "family"])
        ]
        if fallback_specialties:
            return fallback_specialties[:1]
        elif available_specialties:
            return [available_specialties[0]]
        else:
            return []


async def recommend_providers(zip_code: str, symptoms: Optional[List[str]] = None, 
                             radius: float = 25.0) -> List[ProviderInfo]:
    """
    Recommend providers based on location and optionally symptoms.
    
    Args:
        zip_code: Patient's zip code
        symptoms: List of patient symptoms (optional)
        radius: Search radius in kilometers
        
    Returns:
        List of recommended providers
    """
    # Get location from zip code
    location = await get_location_from_zip(zip_code)
    
    # Get providers in the area
    providers = await get_providers_by_location(location, radius)
    
    # If symptoms provided, filter by appropriate specialties
    if symptoms:
        relevant_specialties = await map_symptoms_to_specialties(symptoms)
        # Filter providers by specialty
        providers = [
            provider for provider in providers 
            if any(specialty.id in [s.id for s in provider.specialties] 
                  for specialty in relevant_specialties)
        ]
    
    # Calculate distance and sort by proximity
    for provider in providers:
        # TODO: Implement distance calculation
        pass
    
    providers.sort(key=lambda x: x.distance)
    
    return providers


async def connect_providers(selected_providers: List[ProviderInfo]) -> List[ProviderConfirmationInfo]:
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
            confirmation_code="", # Generate a unique code
            status="pending",
            contact_info={
                "phone": provider.phone,
                "email": "provider@example.com", # This would come from the provider data
            }
        )
        confirmations.append(confirmation)
    
    return confirmations
