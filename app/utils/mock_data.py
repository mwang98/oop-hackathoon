"""
This module contains mock data for clinics to simulate a database.
In a production environment, this would be replaced with actual database connections.
"""
from app.models.schemas import ClinicCategory

# Sample clinic data
CLINICS = [
    {
        "id": "clinic-001",
        "name": "City General Medical Center",
        "category": ClinicCategory.GENERAL_PRACTICE,
        "address": "123 Main St, Anytown, AN 12345",
        "phone_number": "+1 (555) 123-4567",
        "supported_insurance": ["Blue Cross", "Aetna", "Cigna", "Medicare"],
        "rating": 4.5
    },
    {
        "id": "clinic-002",
        "name": "Urgent Care Plus",
        "category": ClinicCategory.URGENT_CARE,
        "address": "456 Oak Ave, Anytown, AN 12345",
        "phone_number": "+1 (555) 234-5678",
        "supported_insurance": ["Blue Cross", "UnitedHealthcare", "Medicare", "Medicaid"],
        "rating": 4.2
    },
    {
        "id": "clinic-003",
        "name": "Children's Wellness Center",
        "category": ClinicCategory.PEDIATRICS,
        "address": "789 Elm Blvd, Anytown, AN 12345",
        "phone_number": "+1 (555) 345-6789",
        "supported_insurance": ["Aetna", "Cigna", "UnitedHealthcare", "Medicaid"],
        "rating": 4.8
    },
    {
        "id": "clinic-004",
        "name": "Joint & Spine Specialists",
        "category": ClinicCategory.ORTHOPEDICS,
        "address": "101 Pine St, Anytown, AN 12346",
        "phone_number": "+1 (555) 456-7890",
        "supported_insurance": ["Blue Cross", "Aetna", "Medicare"],
        "rating": 4.6
    },
    {
        "id": "clinic-005",
        "name": "Heart Health Center",
        "category": ClinicCategory.CARDIOLOGY,
        "address": "202 Cedar Ln, Anytown, AN 12346",
        "phone_number": "+1 (555) 567-8901",
        "supported_insurance": ["Cigna", "UnitedHealthcare", "Medicare", "Medicaid"],
        "rating": 4.7
    },
    {
        "id": "clinic-006",
        "name": "Skin & Dermatology Associates",
        "category": ClinicCategory.DERMATOLOGY,
        "address": "303 Maple Dr, Anytown, AN 12347",
        "phone_number": "+1 (555) 678-9012",
        "supported_insurance": ["Blue Cross", "Aetna", "Cigna"],
        "rating": 4.3
    },
    {
        "id": "clinic-007",
        "name": "Women's Health Clinic",
        "category": ClinicCategory.GYNECOLOGY,
        "address": "404 Birch Ave, Anytown, AN 12347",
        "phone_number": "+1 (555) 789-0123",
        "supported_insurance": ["Blue Cross", "UnitedHealthcare", "Medicare"],
        "rating": 4.9
    },
    {
        "id": "clinic-008",
        "name": "Brain & Nerve Specialists",
        "category": ClinicCategory.NEUROLOGY,
        "address": "505 Willow St, Anytown, AN 12348",
        "phone_number": "+1 (555) 890-1234",
        "supported_insurance": ["Aetna", "Cigna", "Medicare", "Medicaid"],
        "rating": 4.4
    },
    {
        "id": "clinic-009",
        "name": "Vision Care Center",
        "category": ClinicCategory.OPHTHALMOLOGY,
        "address": "606 Spruce Blvd, Anytown, AN 12348",
        "phone_number": "+1 (555) 901-2345",
        "supported_insurance": ["Blue Cross", "Cigna", "UnitedHealthcare"],
        "rating": 4.1
    },
    {
        "id": "clinic-010",
        "name": "Mind Wellness Institute",
        "category": ClinicCategory.PSYCHIATRY,
        "address": "707 Aspen Ln, Anytown, AN 12349",
        "phone_number": "+1 (555) 012-3456",
        "supported_insurance": ["Aetna", "UnitedHealthcare", "Medicaid"],
        "rating": 4.0
    }
]

# Symptom to clinic category mapping
SYMPTOM_TO_CATEGORY = {
    "fever": [ClinicCategory.GENERAL_PRACTICE, ClinicCategory.URGENT_CARE],
    "cough": [ClinicCategory.GENERAL_PRACTICE, ClinicCategory.URGENT_CARE],
    "headache": [ClinicCategory.GENERAL_PRACTICE, ClinicCategory.NEUROLOGY],
    "rash": [ClinicCategory.GENERAL_PRACTICE, ClinicCategory.DERMATOLOGY],
    "joint pain": [ClinicCategory.ORTHOPEDICS, ClinicCategory.GENERAL_PRACTICE],
    "chest pain": [ClinicCategory.CARDIOLOGY, ClinicCategory.URGENT_CARE],
    "blurred vision": [ClinicCategory.OPHTHALMOLOGY, ClinicCategory.NEUROLOGY],
    "abdominal pain": [ClinicCategory.GENERAL_PRACTICE, ClinicCategory.URGENT_CARE],
    "anxiety": [ClinicCategory.PSYCHIATRY, ClinicCategory.GENERAL_PRACTICE],
    "depression": [ClinicCategory.PSYCHIATRY],
    "sore throat": [ClinicCategory.GENERAL_PRACTICE, ClinicCategory.URGENT_CARE],
    "ear pain": [ClinicCategory.GENERAL_PRACTICE],
    "menstrual issues": [ClinicCategory.GYNECOLOGY],
    "pregnancy": [ClinicCategory.GYNECOLOGY],
    "heart palpitations": [ClinicCategory.CARDIOLOGY],
    "dizziness": [ClinicCategory.NEUROLOGY, ClinicCategory.GENERAL_PRACTICE],
    "nausea": [ClinicCategory.GENERAL_PRACTICE, ClinicCategory.URGENT_CARE],
    "vomiting": [ClinicCategory.GENERAL_PRACTICE, ClinicCategory.URGENT_CARE],
    "diarrhea": [ClinicCategory.GENERAL_PRACTICE, ClinicCategory.URGENT_CARE],
    "constipation": [ClinicCategory.GENERAL_PRACTICE],
    "back pain": [ClinicCategory.ORTHOPEDICS, ClinicCategory.GENERAL_PRACTICE],
    "fatigue": [ClinicCategory.GENERAL_PRACTICE],
    "insomnia": [ClinicCategory.PSYCHIATRY, ClinicCategory.GENERAL_PRACTICE],
}

# Mock clinic availability data
CLINIC_AVAILABILITY = {
    "clinic-001": {
        "monday": [{"start": "09:00", "end": "12:00"}, {"start": "13:00", "end": "17:00"}],
        "tuesday": [{"start": "09:00", "end": "12:00"}, {"start": "13:00", "end": "17:00"}],
        "wednesday": [{"start": "09:00", "end": "12:00"}, {"start": "13:00", "end": "17:00"}],
        "thursday": [{"start": "09:00", "end": "12:00"}, {"start": "13:00", "end": "17:00"}],
        "friday": [{"start": "09:00", "end": "15:00"}],
        "saturday": [{"start": "10:00", "end": "14:00"}],
        "sunday": []
    },
    "clinic-002": {
        "monday": [{"start": "08:00", "end": "20:00"}],
        "tuesday": [{"start": "08:00", "end": "20:00"}],
        "wednesday": [{"start": "08:00", "end": "20:00"}],
        "thursday": [{"start": "08:00", "end": "20:00"}],
        "friday": [{"start": "08:00", "end": "20:00"}],
        "saturday": [{"start": "08:00", "end": "20:00"}],
        "sunday": [{"start": "08:00", "end": "20:00"}]
    },
    # Add more clinic availability as needed for other clinic IDs
}

# Mock estimated costs for treatments
ESTIMATED_COSTS = {
    "general_practice": {
        "initial_consultation": 150.0,
        "follow_up": 100.0
    },
    "urgent_care": {
        "visit": 200.0,
        "x_ray": 300.0
    },
    "pediatrics": {
        "initial_consultation": 170.0,
        "well_child_check": 120.0
    },
    "orthopedics": {
        "initial_consultation": 250.0,
        "follow_up": 150.0,
        "joint_injection": 350.0
    },
    "cardiology": {
        "initial_consultation": 300.0,
        "ecg": 200.0,
        "echocardiogram": 500.0
    },
    "dermatology": {
        "initial_consultation": 200.0,
        "skin_biopsy": 300.0
    },
    "gynecology": {
        "initial_consultation": 250.0,
        "annual_exam": 200.0
    },
    "neurology": {
        "initial_consultation": 300.0,
        "eeg": 450.0
    },
    "ophthalmology": {
        "initial_consultation": 200.0,
        "comprehensive_eye_exam": 250.0
    },
    "psychiatry": {
        "initial_evaluation": 350.0,
        "follow_up": 200.0
    }
}

# Mock insurance discount rates (percentage reduction)
INSURANCE_DISCOUNT_RATES = {
    "Blue Cross": 0.2,  # 20% discount
    "Aetna": 0.25,
    "Cigna": 0.15,
    "UnitedHealthcare": 0.3,
    "Medicare": 0.5,
    "Medicaid": 0.7
}

# For self-pay patients, we can offer a standard discount
SELF_PAY_DISCOUNT = 0.1  # 10% discount
