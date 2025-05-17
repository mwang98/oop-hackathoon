# Project Structure for Provider Finder Backend

## Core Modules

### 1. Provider Recommendation
- Input: Zip code
- Output: List[ProviderInfo]

### 2. Provider Connection
- Input: List[ProviderInfo]
- Output: List[ProviderConfirmationInfo]

## Helper Functions

### 1. Geolocation
- Input: Zip code
- Output: Latitude/Longitude

### 2. Provider Search
- Input: Latitude/Longitude, Radius
- Output: List[ProviderInfo]

### 3. Symptom Matching
- Input: Symptoms
- Output: List[ProviderSpecialty]

## Implementation Plan
1. Create data models
2. Implement helper functions
3. Implement core business logic
4. Add API endpoints
5. Test functionality
