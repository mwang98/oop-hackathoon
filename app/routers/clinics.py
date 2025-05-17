"""
API routes for clinic operations.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.models.schemas import (
    PatientInfo, ClinicInfo, ClinicRecommendation, 
    AvailabilityResponse, AppointmentConfirmation
)
from app.services.clinic_service import (
    filter_clinics_by_symptoms, 
    get_clinic_availability,
    get_clinic_recommendations,
    confirm_appointment
)

router = APIRouter(
    prefix="/clinics",
    tags=["clinics"],
    responses={404: {"description": "Not found"}},
)


@router.post("/search", response_model=List[ClinicInfo])
async def search_clinics(
    patient_info: PatientInfo,
    max_distance: Optional[float] = Query(50.0, description="Maximum distance in kilometers")
):
    """
    Search for clinics based on patient symptoms, insurance, and location.
    
    Args:
        patient_info: Patient information including symptoms, insurance, and address
        max_distance: Maximum distance in kilometers
        
    Returns:
        List of matching clinics
    """
    clinics = await filter_clinics_by_symptoms(patient_info, max_distance)
    if not clinics:
        raise HTTPException(
            status_code=404,
            detail="No clinics found matching your criteria. Try expanding your search parameters."
        )
    return clinics


@router.post("/{clinic_id}/availability", response_model=AvailabilityResponse)
async def check_clinic_availability(
    clinic_id: str,
    patient_info: PatientInfo
):
    """
    Check availability and cost information for a specific clinic.
    
    Args:
        clinic_id: ID of the clinic
        patient_info: Patient information
        
    Returns:
        Availability and cost information
    """
    availability = await get_clinic_availability(clinic_id, patient_info)
    if not availability:
        raise HTTPException(
            status_code=404,
            detail=f"Clinic with ID {clinic_id} not found or has no available slots matching your schedule."
        )
    return availability


@router.post("/recommendations", response_model=List[ClinicRecommendation])
async def get_recommendations(
    patient_info: PatientInfo,
    limit: Optional[int] = Query(3, description="Maximum number of recommendations")
):
    """
    Get personalized clinic recommendations.
    
    Args:
        patient_info: Patient information
        limit: Maximum number of recommendations to return
        
    Returns:
        List of clinic recommendations with personalized reasons
    """
    # First, search for suitable clinics
    clinics = await filter_clinics_by_symptoms(patient_info)
    if not clinics:
        raise HTTPException(
            status_code=404,
            detail="No clinics found matching your criteria. Try expanding your search parameters."
        )
    
    # Generate recommendations
    recommendations = await get_clinic_recommendations(clinics, patient_info, limit)
    if not recommendations:
        raise HTTPException(
            status_code=404,
            detail="Could not generate recommendations. Please try different search criteria."
        )
    
    return recommendations


@router.post("/{clinic_id}/confirm", response_model=AppointmentConfirmation)
async def confirm_clinic_appointment(
    clinic_id: str,
    patient_info: PatientInfo,
    slot: dict
):
    """
    Confirm an appointment with a clinic.
    
    Args:
        clinic_id: ID of the clinic
        patient_info: Patient information
        slot: Selected appointment slot
        
    Returns:
        Appointment confirmation details
    """
    result = await confirm_appointment(clinic_id, patient_info, slot)
    
    if result["status"] == "failed":
        raise HTTPException(
            status_code=400,
            detail=result["message"]
        )
    
    return AppointmentConfirmation(
        clinic_id=clinic_id,
        patient_name=result["patient_name"],
        appointment_date=result["appointment_date"],
        status=result["status"],
        confirmation_code=result["confirmation_code"],
        additional_info=result["additional_info"]
    )
