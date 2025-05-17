"""
API routes for appointment operations.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict
from app.models.schemas import AppointmentConfirmation

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{confirmation_code}", response_model=Dict)
async def get_appointment(
    confirmation_code: str
):
    """
    Get details of an existing appointment.
    
    Args:
        confirmation_code: Unique confirmation code for the appointment
        
    Returns:
        Appointment details
    """
    # In a real application, this would query a database
    # For this demo, we'll return a mock response
    
    # Check if confirmation code is valid (should be CONF-XXXXX format)
    if not confirmation_code.startswith("CONF-") or len(confirmation_code) != 10:
        raise HTTPException(
            status_code=404,
            detail="Invalid confirmation code."
        )
    
    # Mock appointment data
    # In a real application, this would be retrieved from a database
    return {
        "confirmation_code": confirmation_code,
        "status": "confirmed",
        "message": "Your appointment is confirmed. Please arrive 15 minutes early."
    }


@router.delete("/{confirmation_code}", response_model=Dict)
async def cancel_appointment(
    confirmation_code: str,
    reason: Optional[str] = Query(None, description="Reason for cancellation")
):
    """
    Cancel an existing appointment.
    
    Args:
        confirmation_code: Unique confirmation code for the appointment
        reason: Optional reason for cancellation
        
    Returns:
        Cancellation status
    """
    # In a real application, this would update a database
    # For this demo, we'll return a mock response
    
    # Check if confirmation code is valid (should be CONF-XXXXX format)
    if not confirmation_code.startswith("CONF-") or len(confirmation_code) != 10:
        raise HTTPException(
            status_code=404,
            detail="Invalid confirmation code."
        )
    
    return {
        "confirmation_code": confirmation_code,
        "status": "cancelled",
        "message": "Your appointment has been successfully cancelled.",
        "reason": reason or "No reason provided"
    }


@router.put("/{confirmation_code}/reschedule", response_model=Dict)
async def reschedule_appointment(
    confirmation_code: str,
    new_slot: Dict
):
    """
    Reschedule an existing appointment.
    
    Args:
        confirmation_code: Unique confirmation code for the appointment
        new_slot: New appointment slot
        
    Returns:
        Updated appointment details
    """
    # In a real application, this would update a database
    # For this demo, we'll return a mock response
    
    # Check if confirmation code is valid (should be CONF-XXXXX format)
    if not confirmation_code.startswith("CONF-") or len(confirmation_code) != 10:
        raise HTTPException(
            status_code=404,
            detail="Invalid confirmation code."
        )
    
    # Check if new slot has required fields
    if not new_slot or "day" not in new_slot or "start" not in new_slot:
        raise HTTPException(
            status_code=400,
            detail="Invalid appointment slot. Day and start time are required."
        )
    
    return {
        "confirmation_code": confirmation_code,
        "status": "rescheduled",
        "message": f"Your appointment has been rescheduled to {new_slot['day']} at {new_slot['start']}.",
        "new_slot": new_slot
    }
