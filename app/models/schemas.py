from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional, Dict
from datetime import datetime, time


class SymptomSeverity(str, Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class Symptom(BaseModel):
    name: str
    severity: SymptomSeverity
    duration_days: Optional[int] = None
    description: Optional[str] = None


class DayOfWeek(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class TimeSlot(BaseModel):
    start_time: time
    end_time: time


class Availability(BaseModel):
    day_of_week: DayOfWeek
    time_slots: List[TimeSlot]


class InsuranceType(str, Enum):
    PRIVATE = "private"
    MEDICARE = "medicare"
    MEDICAID = "medicaid"
    SELF_PAY = "self_pay"


class InsurancePolicy(BaseModel):
    provider: str
    policy_id: str
    type: InsuranceType
    group_number: Optional[str] = None
    additional_details: Optional[Dict] = None


class PatientInfo(BaseModel):
    name: str
    date_of_birth: datetime
    symptoms: List[Symptom]
    availability: List[Availability]
    insurance: InsurancePolicy
    address: str = Field(..., description="Patient's address for distance calculation")
    contact_number: str
    email: Optional[str] = None


class ClinicCategory(str, Enum):
    GENERAL_PRACTICE = "general_practice"
    URGENT_CARE = "urgent_care"
    PEDIATRICS = "pediatrics"
    ORTHOPEDICS = "orthopedics"
    CARDIOLOGY = "cardiology"
    DERMATOLOGY = "dermatology"
    GYNECOLOGY = "gynecology"
    NEUROLOGY = "neurology"
    OPHTHALMOLOGY = "ophthalmology"
    PSYCHIATRY = "psychiatry"
    OTHER = "other"


class ClinicInfo(BaseModel):
    id: str
    name: str
    category: ClinicCategory
    address: str
    phone_number: str
    supported_insurance: List[str]
    rating: Optional[float] = None
    distance_km: Optional[float] = None


class AvailabilityResponse(BaseModel):
    clinic_id: str
    available_slots: List[Dict[str, time]]
    estimated_cost: float


class ClinicRecommendation(BaseModel):
    clinic: ClinicInfo
    recommendation_reason: str
    available_slots: Optional[List[Dict[str, time]]] = None
    estimated_cost: Optional[float] = None


class AppointmentConfirmation(BaseModel):
    clinic_id: str
    patient_name: str
    appointment_date: datetime
    status: str
    confirmation_code: Optional[str] = None
    additional_info: Optional[str] = None
