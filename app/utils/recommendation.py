"""
Utility functions for generating recommendations using OpenAI.
"""
import os
import openai
import logging
from typing import List, Dict
from app.models.schemas import ClinicInfo, PatientInfo

# Configure logger
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def generate_recommendation_reason(
    clinic: ClinicInfo, 
    patient_info: PatientInfo, 
    available_slots: List[Dict],
    estimated_cost: float
) -> str:
    """
    Generate a personalized recommendation reason for a clinic.
    
    Args:
        clinic: Clinic information
        patient_info: Patient information
        available_slots: Available appointment slots
        estimated_cost: Estimated cost for the appointment
    
    Returns:
        String containing the recommendation reason
    """
    try:
        # Construct a prompt for the OpenAI model
        prompt = f"""
        Generate a personalized clinic recommendation for a patient based on the following information:
        
        Patient Symptoms: {', '.join([s.name for s in patient_info.symptoms])}
        
        Clinic Information:
        - Name: {clinic.name}
        - Category: {clinic.category.value}
        - Rating: {clinic.rating}
        - Distance: {clinic.distance_km} km from patient
        - Accepts patient's insurance: {patient_info.insurance.provider in clinic.supported_insurance}
        
        Available appointment slots: {len(available_slots)} slots available
        Estimated cost: ${estimated_cost:.2f}
        
        Give a brief, personalized reason (3-5 sentences) why this clinic would be a good match for the patient,
        focusing on the clinic's strengths related to the patient's symptoms and practical considerations like
        insurance coverage, distance, and availability.
        """
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a healthcare assistant providing clinic recommendations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        
        # Extract and return the recommendation
        recommendation = response.choices[0].message.content.strip()
        return recommendation
    
    except Exception as e:
        logger.error(f"Error generating recommendation: {str(e)}")
        # Fallback recommendation if the API call fails
        return f"{clinic.name} is a {clinic.rating}-star clinic located {clinic.distance_km} km away that specializes in {clinic.category.value}. They accept your insurance and have availability that matches your schedule."
