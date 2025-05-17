"""
Service module for clinic-related operations.
"""
from typing import List, Dict, Set, Optional
import logging
import random
from datetime import datetime, time
from app.models.schemas import (
    PatientInfo, ClinicInfo, ClinicCategory, 
    ClinicRecommendation, AvailabilityResponse
)
from app.utils.mock_data import (
    CLINICS, SYMPTOM_TO_CATEGORY, CLINIC_AVAILABILITY,
    ESTIMATED_COSTS, INSURANCE_DISCOUNT_RATES, SELF_PAY_DISCOUNT
)
from app.utils.geo_utils import calculate_distance
from app.utils.recommendation import generate_recommendation_reason

# Configure logger
logger = logging.getLogger(__name__)


async def filter_clinics_by_symptoms(
    patient_info: PatientInfo,
    max_distance: float = 50.0  # Default max distance in km
) -> List[ClinicInfo]:
    """
    Filter clinics based on patient symptoms, insurance, and distance.
    
    Args:
        patient_info: Patient information including symptoms and insurance
        max_distance: Maximum distance in kilometers
        
    Returns:
        List of filtered clinic information
    """
    # Extract symptom names
    symptom_names = [symptom.name.lower() for symptom in patient_info.symptoms]
    
    # Determine relevant clinic categories based on symptoms
    relevant_categories: Set[ClinicCategory] = set()
    for symptom in symptom_names:
        for category_keyword, categories in SYMPTOM_TO_CATEGORY.items():
            if category_keyword in symptom:
                relevant_categories.update(categories)
    
    # If no specific categories found, default to general practice and urgent care
    if not relevant_categories:
        relevant_categories = {ClinicCategory.GENERAL_PRACTICE, ClinicCategory.URGENT_CARE}
    
    # Filter clinics by category and insurance
    filtered_clinics = []
    for clinic_data in CLINICS:
        # Check if clinic category matches
        if clinic_data["category"] not in relevant_categories:
            continue
        
        # Check if insurance is accepted
        if patient_info.insurance.provider not in clinic_data["supported_insurance"] and \
           patient_info.insurance.type.value != "self_pay":
            continue
        
        # Calculate distance
        distance = calculate_distance(patient_info.address, clinic_data["address"])
        if distance is None or distance > max_distance:
            continue
        
        # Create ClinicInfo object with distance
        clinic = ClinicInfo(**clinic_data)
        clinic.distance_km = distance
        filtered_clinics.append(clinic)
    
    # Sort by distance
    filtered_clinics.sort(key=lambda x: x.distance_km or float('inf'))
    
    return filtered_clinics


async def get_clinic_availability(
    clinic_id: str,
    patient_info: PatientInfo
) -> Optional[AvailabilityResponse]:
    """
    Get availability and cost information for a specific clinic.
    
    Args:
        clinic_id: ID of the clinic
        patient_info: Patient information
        
    Returns:
        AvailabilityResponse object or None if clinic is not found
    """
    # Check if clinic exists
    clinic_data = next((c for c in CLINICS if c["id"] == clinic_id), None)
    if not clinic_data:
        return None
    
    # Find clinic availability
    clinic_schedule = CLINIC_AVAILABILITY.get(clinic_id, {})
    
    # Get patient available days
    patient_availability = {avail.day_of_week.value.lower(): avail.time_slots for avail in patient_info.availability}
    
    # Find matching available slots
    available_slots = []
    for day, slots in clinic_schedule.items():
        if day in patient_availability:
            patient_slots = patient_availability[day]
            for clinic_slot in slots:
                clinic_start = datetime.strptime(clinic_slot["start"], "%H:%M").time()
                clinic_end = datetime.strptime(clinic_slot["end"], "%H:%M").time()
                
                for patient_slot in patient_slots:
                    # Check if there's an overlap
                    if (patient_slot.start_time <= clinic_end and 
                        patient_slot.end_time >= clinic_start):
                        # Calculate the overlapping time period
                        overlap_start = max(patient_slot.start_time, clinic_start)
                        overlap_end = min(patient_slot.end_time, clinic_end)
                        
                        # Only include if there's a meaningful overlap (e.g., at least 30 minutes)
                        time_difference = (
                            datetime.combine(datetime.today(), overlap_end) - 
                            datetime.combine(datetime.today(), overlap_start)
                        ).seconds / 60
                        
                        if time_difference >= 30:
                            available_slots.append({
                                "day": day,
                                "start": overlap_start,
                                "end": overlap_end
                            })
    
    # Calculate estimated cost
    base_cost = ESTIMATED_COSTS.get(
        clinic_data["category"].value, 
        {"initial_consultation": 200.0}
    ).get("initial_consultation", 200.0)
    
    # Apply insurance discount if applicable
    if patient_info.insurance.type.value != "self_pay" and patient_info.insurance.provider in clinic_data["supported_insurance"]:
        discount_rate = INSURANCE_DISCOUNT_RATES.get(patient_info.insurance.provider, 0.0)
        estimated_cost = base_cost * (1 - discount_rate)
    else:
        # Apply self-pay discount
        estimated_cost = base_cost * (1 - SELF_PAY_DISCOUNT)
    
    return AvailabilityResponse(
        clinic_id=clinic_id,
        available_slots=available_slots,
        estimated_cost=round(estimated_cost, 2)
    )


async def get_clinic_recommendations(
    clinics: List[ClinicInfo],
    patient_info: PatientInfo,
    limit: int = 3
) -> List[ClinicRecommendation]:
    """
    Generate personalized recommendations for clinics.
    
    Args:
        clinics: List of filtered clinics
        patient_info: Patient information
        limit: Maximum number of recommendations to generate
        
    Returns:
        List of ClinicRecommendation objects
    """
    recommendations = []
    
    # Limit the number of clinics to process
    clinics_to_process = clinics[:limit]
    
    for clinic in clinics_to_process:
        # Get availability and cost information
        availability_info = await get_clinic_availability(clinic.id, patient_info)
        
        if availability_info and availability_info.available_slots:
            # Generate recommendation reason
            recommendation_reason = await generate_recommendation_reason(
                clinic,
                patient_info,
                availability_info.available_slots,
                availability_info.estimated_cost
            )
            
            # Create recommendation object
            recommendation = ClinicRecommendation(
                clinic=clinic,
                recommendation_reason=recommendation_reason,
                available_slots=availability_info.available_slots,
                estimated_cost=availability_info.estimated_cost
            )
            
            recommendations.append(recommendation)
    
    return recommendations


async def confirm_appointment(
    clinic_id: str,
    patient_info: PatientInfo,
    selected_slot: Dict
) -> Dict:
    """
    Confirm an appointment with a clinic.
    
    Args:
        clinic_id: ID of the selected clinic
        patient_info: Patient information
        selected_slot: Selected appointment slot
        
    Returns:
        Dictionary with confirmation status and details
    """
    # In a real application, this would contact the clinic's booking system
    # For this demo, we'll simulate a successful booking
    
    # Check if clinic exists
    clinic_data = next((c for c in CLINICS if c["id"] == clinic_id), None)
    if not clinic_data:
        return {
            "status": "failed",
            "message": "Clinic not found"
        }
    
    # Generate a confirmation code
    confirmation_code = f"CONF-{random.randint(10000, 99999)}"
    
    # Format the appointment date
    day_of_week = selected_slot["day"]
    start_time = selected_slot["start"]
    
    # In a real application, we would convert this to an actual date
    appointment_date = f"Next {day_of_week.capitalize()} at {start_time.strftime('%H:%M')}"
    
    return {
        "status": "confirmed",
        "clinic_name": clinic_data["name"],
        "patient_name": patient_info.name,
        "appointment_date": appointment_date,
        "confirmation_code": confirmation_code,
        "additional_info": f"Please arrive 15 minutes early and bring your insurance card. Call {clinic_data['phone_number']} if you need to reschedule."
    }
