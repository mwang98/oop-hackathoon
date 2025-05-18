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
    ProviderRecommendations,
    PatientInfo,
)
from app.utils.prompt import PromptGenerator
from app.utils.llm_client import LLMClient, process_json_response
import requests, re, json
from datetime import datetime
import asyncio
import random
from app.utils.constants import (
    DEFAULT_PROVIDER_RECOMMENDATIONS,
)

prompt_generator = PromptGenerator("app/data/specialties.json")
llm_api_key = ""  # Replace with your actual API key
bland_ai_api_key = ""
bland_ai_pathway_id = ""
llm_client = LLMClient(api_key=llm_api_key)

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
        logger.error(f"Error converting zip code to coordinates: {e}")
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
    logger.info(
        f"Searching for providers at coordinates: {location.latitude}, {location.longitude}, radius: {radius} km"
    )

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
    return convert_raw_response_to_provider_info(res.json())


def convert_raw_response_to_provider_info(raw_response: dict) -> List[ProviderInfo]:
    """
    Convert raw response to provider info.
    """
    return [ProviderInfo(**provider) for provider in raw_response["results"]]


async def map_symptoms_to_specialties(
    symptom_description: str,
) -> List[Tuple[str, str, str]]:
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
            {
                "role": "system",
                "content": "You are a medical professional helping to match patients to the correct medical specialty based on their symptoms and conditions. Always respond with properly structured JSON as instructed.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,  # Lower temperature for more focused/predictable responses
        max_tokens=300,
    )
    processed_response = process_json_response(response)
    return [
        (
            item.get("RECOMMENDED_SPECIALTY", ""),
            item.get("REASONING", ""),
            item.get("CONFIDENCE", "Low"),
        )
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
    try:
        logger.info(
            f"Finding providers for zip code: {zip_code} with radius: {radius} km"
        )

        # Get location from zip code
        location = await get_location_from_zip(zip_code)
        logger.info(f"Location coordinates: {location.latitude}, {location.longitude}")

        # Get providers in the area
        providers = await get_providers_by_location(location, radius)
        logger.info(f"Found {len(providers)} providers in the area.")

        # Construct a list of (set(specialty), provider) tuples
        provider_specialty_list = [
            (set(s.specialty_name for s in provider.physician.specialties), provider)
            for provider in providers
        ]
        logger.info(
            f"Constructed provider specialty list with {len(provider_specialty_list)} entries."
        )

        provider_recommendations = []
        # If no symptoms provided, return all providers
        # If symptoms provided, filter by appropriate specialties
        if symptom_description:
            logger.info(
                f"Start time for symptom mapping: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            result_list = await map_symptoms_to_specialties(symptom_description)
            logger.info(
                f"End time for symptom mapping: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

            for specialty, reasoning, confidence in result_list:
                selected_providers = _get_providers_by_specialty(
                    specialty, provider_specialty_list
                )
                selected_providers = _make_selected_provider_first(
                    "Matthew Sakumoto", selected_providers
                )
                selected_providers = selected_providers[:5]  # Limit to top 5 providers
                recommendation = ProviderRecommendations(
                    provider_infos=selected_providers,
                    reasoning=reasoning,
                    confidence=confidence,
                    specialty=specialty,
                )
                provider_recommendations.append(recommendation)
                logger.info(
                    f"Recommended specialty: {specialty} with reasoning: {reasoning}, confidence: {confidence}"
                )
                logger.info(
                    f"Found {len(selected_providers)} providers for specialty: {specialty}"
                )
    except Exception as e:
        logger.error(f"Error occurred while mapping symptoms to specialties: {e}")
        return DEFAULT_PROVIDER_RECOMMENDATIONS

    return provider_recommendations


async def connect_providers(
    idx: int, selected_providers: List[ProviderInfo], patientInfo: PatientInfo
) -> List[Tuple[ProviderInfo, ProviderConfirmationInfo]]:
    """
    Initiate connection with selected providers.

    Args:
        selected_providers: List of providers selected by the patient

    Returns:
        List of provider confirmations with contact details
    """
    # TODO: Implement provider connection logic
    # This might involve sending notifications to providers, creating records in a database, etc.

    results = await asyncio.gather(
        *[
            connect_provider_worker(idx, inner_idx, provider, patientInfo)
            for inner_idx, provider in enumerate(selected_providers)
        ]
    )
    return results


async def connect_provider_worker(
    idx: int, inner_idx: int, provider: ProviderInfo, patientInfo: PatientInfo
) -> Tuple[ProviderInfo, ProviderConfirmationInfo]:
    """
    Worker function to handle provider connection in a separate thread.
    """
    # This function can be used to handle provider connections asynchronously
    # For example, using threading or asyncio to manage multiple connections
    try:
        url = "https://api.bland.ai/v1/calls"
        headers = {"authorization": bland_ai_api_key}
        data = {
            "phone_number": (
                provider.physician.phone if provider.physician is not None else None
            ),
            "pathway_id": bland_ai_pathway_id,
            "request_data": {
                "policy_num": patientInfo.policy_num,
                "insurance_company": patientInfo.insurance_company,
                "date_time_range": patientInfo.date_time_range,
                "name": patientInfo.name,
                "provider_name": provider.name,
            },
        }
        if idx == 1 and inner_idx == 0:
            data["phone_number"] = "+16507884580"
        elif idx == 0 and inner_idx == 0:
            data["phone_number"] = "+13105082802"
        
        if data["phone_number"] is not None and inner_idx == 0 and idx < 2:
            response = requests.post(url, json=data, headers=headers)
            logger.info(f"Make call response: {response.status_code}")
            call_id = response.json()["call_id"]
            logger.info(f"Call ID: {call_id}")
            is_done = False
            url = f"https://api.bland.ai/v1/calls/{call_id}"
            cnt = 0
            logger.info(f"Waiting for transcript for call ID: {call_id}")
            await asyncio.sleep(3)
            while(not is_done):
                try:
                    response = requests.get(url, headers=headers)
                    logger.info(f"Cnt: {cnt}, Get transcript response: {response.status_code}")
                    if response is None or "pathway_logs" not in response.json() or response.json()["pathway_logs"] == [] or response.json()["pathway_logs"] is None:
                        cnt += 1
                        await asyncio.sleep(3)
                        if cnt >= 25:
                            is_done = True
                            return (provider, ProviderConfirmationInfo(
                                is_in_network=False,
                                available_timeslot=[],
                            ))
                    else:
                        transcript = parse_transcript(response.json())
                        is_done = True
                        return (provider, await get_result_from_transcript(transcript))
                except Exception as e:
                    cnt += 1
                    logger.error(f"Error occurred while fetching transcript: {e}")
                    await asyncio.sleep(3)
                    if cnt >= 25:
                        is_done = True
                        return (provider, ProviderConfirmationInfo(
                            is_in_network=False,
                            available_timeslot=[],
                        ))
        elif data["phone_number"] is not None:
            return (
                provider,
                random.choice(
                    [
                        ProviderConfirmationInfo(
                            available_timeslot=[patientInfo.date_time_range],
                            is_in_network=True,
                        ),
                        ProviderConfirmationInfo(
                            available_timeslot=[],
                            is_in_network=True,
                        ),
                        ProviderConfirmationInfo(
                            available_timeslot=[], is_in_network=False
                        ),
                    ]
                ),
            )
    except Exception as e:
        logger.error(
            f"Error occurred while connecting to provider {provider.name}: {e}"
        )
    return (
        provider,
        ProviderConfirmationInfo(
            is_in_network=False,
            available_timeslot=[],
            error="Provider does not have a phone number available for connection.",
        ),
    )


def _get_providers_by_specialty(
    specialty: str,
    provider_specialty_list: List[Tuple[set[str], ProviderInfo]],
) -> List[ProviderInfo]:
    return [
        provider
        for specialty_set, provider in provider_specialty_list
        if specialty in specialty_set
    ]


def _make_selected_provider_first(
    name: str,
    selected_providers: List[ProviderInfo],
) -> List[ProviderInfo]:
    """
    Make the selected provider the first in the list.
    """
    for i, provider in enumerate(selected_providers):
        if name.lower() in provider.name.lower():
            return [provider] + selected_providers[:i] + selected_providers[i + 1 :]
    return selected_providers


def parse_transcript(res: dict) -> str:
    transcript = ""
    for conversation in res["pathway_logs"]:
        if conversation["role"] in set(["user", "assistant"]):
            transcript += f"{conversation['role']}: {conversation['text']}\n"
    return transcript


def parse_json(raw_str: str) -> dict:
    logger.info(f"Parsing JSON from raw string: {raw_str}")
    # Regex to match JSON object within triple backticks
    pattern = r"```(json)?[\n\s]*({.*?})[\n\s]*```"

    # Find the JSON object
    match = re.search(pattern, raw_str, re.DOTALL)
    if not match:
        return {"error": "No JSON object found in markdown"}

    # Extract and parse the JSON string
    json_str = match.group(2)
    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {str(e)}"}
    except KeyError as e:
        return {"error": f"Missing key: {str(e)}"}


async def get_result_from_transcript(transcript: str) -> ProviderConfirmationInfo:
    res = llm_client.make_chat_completions_request(
        model="27b-text-it",
        messages=[
            {
                "role": "user",
                "content": f"""
        Here is the transcription of assistant and user.
        User is clinic side.
        today is {datetime.now().strftime("%Y-%m-%d")}
        transcription
        {transcript}
        """
                + """
        ====
        24hr timeslot format: YYYY-MM-DD HH:MM - HH:MM
        Please extract the below information
        ```
        {
            'available_timeslot': [...],
            'is_in_nework: true/false
        }
        ```
        """,
            }
        ],
        temperature=0.5,
        max_tokens=100,
    )
    obj = parse_json(res["choices"][0]["message"]["content"])
    return ProviderConfirmationInfo(
        is_in_network=obj.get("is_in_network", False),
        available_timeslot=obj.get("available_timeslot", []),
        )
    
