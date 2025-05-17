# Clinic Finder APIA FastAPI-based backend for finding and booking clinic appointments based on patient needs.## Features### 1. Clinic Candidate Selection- Finds clinics that match patient symptoms- Filters by insurance acceptance- Considers proximity to patient- Returns a list of suitable clinics### 2. Calling Clinic for Information- Provides availability information for selected clinics- Estimates treatment costs based on insurance- Shows available time slots matching patient's schedule

### 3. Clinic Recommendation
- Generates personalized recommendations using AI
- Explains why each clinic is a good match
- Considers symptoms, insurance, distance, and availability

### 4. Appointment Confirmation
- Simulates booking appointments with clinics
- Provides confirmation codes
- Supports appointment management (viewing, cancelling, rescheduling)

## Technical Stack

- **Framework**: FastAPI
- **Data Validation**: Pydantic
- **AI Recommendations**: OpenAI
- **Geocoding**: GeoPy for distance calculations
- **Testing**: Pytest

## Project Structure

```
/app
  /models       - Pydantic models for data validation
  /routers      - API route definitions
  /services     - Business logic
  /utils        - Utility functions
/tests          - Test cases
requirements.txt - Dependencies
run.py          - Entry point
.env.example    - Environment variable template
```

## API Endpoints

### Clinic Search
- `POST /api/v1/clinics/search` - Find clinics based on patient info

### Clinic Information
- `POST /api/v1/clinics/{clinic_id}/availability` - Get availability & cost info

### Recommendations
- `POST /api/v1/clinics/recommendations` - Get personalized clinic recommendations

### Appointments
- `POST /api/v1/clinics/{clinic_id}/confirm` - Book an appointment
- `GET /api/v1/appointments/{confirmation_code}` - Get appointment details
- `DELETE /api/v1/appointments/{confirmation_code}` - Cancel appointment
- `PUT /api/v1/appointments/{confirmation_code}/reschedule` - Reschedule appointment

## Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key (for recommendation generation)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env file to add your OpenAI API key
```

### Running the Application

```bash
python run.py
```

The API will be available at http://localhost:8000

API documentation will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Running Tests

```bash
pytest
```

## Data Models

### Patient Information
- Name
- Date of birth
- Symptoms (with severity and duration)
- Availability (days and time slots)
- Insurance details
- Address
- Contact information

### Clinic Information
- ID
- Name
- Category/Specialization
- Address
- Phone number
- Supported insurance providers
- Rating
- Distance from patient

## Notes

- This implementation uses mock data for demonstration purposes
- In a production environment, you would connect to real databases and APIs
- The OpenAI integration requires a valid API key to generate recommendations
