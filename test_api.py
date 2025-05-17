#!/usr/bin/env python3
"""
Script to test the Clinic Finder API endpoints.
Run this script with the API server running.
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def print_response(response):
    """Pretty print the API response"""
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    print("Response Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print("-" * 80)

def test_root():
    """Test the root endpoint"""
    print("\n🔍 Testing root endpoint")
    response = requests.get("http://localhost:8000/")
    print_response(response)

def test_search_clinics():
    """Test the search clinics endpoint"""
    print("\n🔍 Testing clinic search")
    
    patient_data = {
        "name": "Test Patient",
        "date_of_birth": datetime.now().isoformat(),
        "symptoms": [
            {"name": "headache", "severity": "moderate", "duration_days": 2}
        ],
        "availability": [
            {
                "day_of_week": "monday",
                "time_slots": [
                    {"start_time": "09:00:00", "end_time": "17:00:00"}
                ]
            }
        ],
        "insurance": {
            "provider": "Blue Cross",
            "policy_id": "BC123456",
            "type": "private"
        },
        "address": "123 Test St, Anytown, AN 12345",
        "contact_number": "+1 (555) 123-4567"
    }
    
    response = requests.post(f"{BASE_URL}/clinics/search", json=patient_data)
    print_response(response)
    
    # Return the response for use in other tests
    return response.json() if response.status_code == 200 else None

def test_clinic_availability(clinic_id):
    """Test the clinic availability endpoint"""
    print(f"\n🔍 Testing clinic availability for clinic {clinic_id}")
    
    patient_data = {
        "name": "Test Patient",
        "date_of_birth": datetime.now().isoformat(),
        "symptoms": [
            {"name": "headache", "severity": "moderate", "duration_days": 2}
        ],
        "availability": [
            {
                "day_of_week": "monday",
                "time_slots": [
                    {"start_time": "09:00:00", "end_time": "17:00:00"}
                ]
            }
        ],
        "insurance": {
            "provider": "Blue Cross",
            "policy_id": "BC123456",
            "type": "private"
        },
        "address": "123 Test St, Anytown, AN 12345",
        "contact_number": "+1 (555) 123-4567"
    }
    
    response = requests.post(f"{BASE_URL}/clinics/{clinic_id}/availability", json=patient_data)
    print_response(response)
    
    return response.json() if response.status_code == 200 else None

def test_recommendations():
    """Test the clinic recommendations endpoint"""
    print("\n🔍 Testing clinic recommendations")
    
    patient_data = {
        "name": "Test Patient",
        "date_of_birth": datetime.now().isoformat(),
        "symptoms": [
            {"name": "headache", "severity": "moderate", "duration_days": 2}
        ],
        "availability": [
            {
                "day_of_week": "monday",
                "time_slots": [
                    {"start_time": "09:00:00", "end_time": "17:00:00"}
                ]
            }
        ],
        "insurance": {
            "provider": "Blue Cross",
            "policy_id": "BC123456",
            "type": "private"
        },
        "address": "123 Test St, Anytown, AN 12345",
        "contact_number": "+1 (555) 123-4567"
    }
    
    response = requests.post(f"{BASE_URL}/clinics/recommendations", json=patient_data)
    print_response(response)

def main():
    """Run all the tests"""
    print("🏥 Testing Clinic Finder API 🏥")
    print("Make sure the API server is running!")
    
    # Test the root endpoint
    test_root()
    
    # Test search clinics
    clinics = test_search_clinics()
    
    # Test clinic availability if search returned results
    if clinics and len(clinics) > 0:
        clinic_id = clinics[0]["id"]
        availability = test_clinic_availability(clinic_id)
    
    # Test recommendations
    test_recommendations()

if __name__ == "__main__":
    main()
