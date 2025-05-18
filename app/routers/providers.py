"""
API routes for provider finder operations.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.schemas import ProviderInfo, ProviderConfirmationInfo, ProviderRecommendations
from app.services.provider_service import recommend_providers, connect_providers

router = APIRouter(
    prefix="/providers",
    tags=["providers"],
    responses={404: {"description": "Not found"}},
)


@router.get("/recommend", response_model=List[ProviderRecommendations])
async def get_provider_recommendations(
    zip_code: str,
    symptom_description: Optional[str] = Query(None, description="Patient's symptom description"),
    radius: Optional[float] = Query(25.0, description="Search radius in kilometers")
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
    providers = await recommend_providers(zip_code, symptom_description, radius)
    if not providers:
        raise HTTPException(
            status_code=404,
            detail="No providers found matching your criteria. Try expanding your search radius."
        )
    return providers


@router.post("/connect", response_model=List[ProviderConfirmationInfo])
async def connect_to_providers(
    selected_providers: List[ProviderInfo]
):
    """
    Connect with selected providers.
    
    Args:
        selected_providers: List of providers selected by the patient
        
    Returns:
        List of provider confirmation details
    """
    confirmations = await connect_providers(selected_providers)
    if not confirmations:
        raise HTTPException(
            status_code=400,
            detail="Failed to connect with providers. Please try again later."
        )
    return confirmations
