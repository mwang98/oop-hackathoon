"""
API routes for provider finder operations.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.schemas import (
    ProviderInfo,
    ProviderConfirmationInfo,
    ProviderRecommendations,
    PatientInfo,
    Request,
)
from app.services.provider_service import recommend_providers, connect_providers
import asyncio

router = APIRouter(
    prefix="/providers",
    tags=["providers"],
    responses={404: {"description": "Not found"}},
)


@router.post("/recommend", response_model=List[ProviderRecommendations])
async def get_provider_recommendations(
    request: Request,
):
    """
    Recommend providers based on zip code and optional symptoms.

    Args:
        zip_code: Patient's zip code
        symptom_description: Description of patient's symptoms
        radius: Search radius in kilometers

    Returns:
        List of recommended providers
    """
    provider_recommendations = await recommend_providers(
        request.zip_code, request.symptom_description, request.radius
    )

    if not provider_recommendations:
        raise HTTPException(
            status_code=404,
            detail="No providers found matching your criteria. Try expanding your search radius.",
        )
    confirmations = await asyncio.gather(
        *[
            connect_providers_worker(idx, provider_recommendation, request.patient_info)
            for idx, provider_recommendation in enumerate(provider_recommendations)
        ]
    )
    return confirmations


async def connect_providers_worker(
    idx: int, recommendation: ProviderRecommendations, patientInfo: PatientInfo
):
    confirmations = await connect_providers(
        idx, recommendation.provider_infos, patientInfo
    )
    recommendation.provider_confirmation_infos = [
        confirmation[1] for confirmation in confirmations
    ]
    recommendation.provider_infos = [confirmation[0] for confirmation in confirmations]
    return recommendation


@router.post("/connect", response_model=List[ProviderConfirmationInfo])
async def connect_to_providers(
    selected_providers: List[ProviderInfo], patientInfo: PatientInfo
):
    """
    Connect with selected providers.

    Args:
        selected_providers: List of providers selected by the patient

    Returns:
        List of provider confirmation details
    """
    confirmations = await connect_providers(selected_providers, patientInfo)
    if not confirmations:
        raise HTTPException(
            status_code=400,
            detail="Failed to connect with providers. Please try again later.",
        )
    return confirmations
