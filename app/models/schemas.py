"""
Schema definitions for provider finder application.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class Location(BaseModel):
    """Location information with latitude and longitude."""
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Specialty(BaseModel):
    """Detailed specialty information."""
    id: Optional[str] = None
    specialty_name: Optional[str] = Field(None, alias="specialtyName")
    specialty_id: Optional[str] = Field(None, alias="specialtyId")
    description: Optional[str] = None
    exclude: Optional[bool] = False
    physician_specialty: Optional[Dict] = Field(None, alias="physicianSpecialty")
    class Config:
        extra = "allow"


class BoardCertification(BaseModel):
    """Board certification information."""
    name: Optional[str] = None
    source: Optional[str] = None


class BoardCertifications(BaseModel):
    """Collection of board certifications."""
    board_certifications: Optional[List[BoardCertification]] = Field(None, alias="boardCertifications")


class Physician(BaseModel):
    """Detailed physician information."""
    name: Optional[str] = None
    date_imported: Optional[str] = Field(None, alias="dateImported")
    hash: Optional[str] = None
    id: Optional[str] = None
    provider_id: Optional[str] = Field(None, alias="providerId")
    address_line1: Optional[str] = Field(None, alias="addressLine1")
    address_city: Optional[str] = Field(None, alias="addressCity")
    address_state: Optional[str] = Field(None, alias="addressState")
    address_zipcode: Optional[str] = Field(None, alias="addressZipcode")
    phone: Optional[str] = None
    geocode_source: Optional[str] = Field(None, alias="geocodeSource")
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    suffix: Optional[str] = None
    gender: Optional[str] = None
    medical_school_name: Optional[str] = Field(None, alias="medicalSchoolName")
    graduation_year: Optional[str] = Field(None, alias="graduationYear")
    telehealth: Optional[bool] = Field(None, alias="telehealth")
    organization_name: Optional[str] = Field(None, alias="organizationName")
    group_practice_pac_id: Optional[str] = Field(None, alias="groupPracticePacId")
    group_accepts_medicare_assignment: Optional[bool] = Field(None, alias="groupAcceptsMedicareAssignment")
    address_line2: Optional[str] = Field(None, alias="addressLine2")
    address_id: Optional[str] = Field(None, alias="addressId")
    address_line2_suppress: Optional[bool] = Field(None, alias="addressLine2suppress")
    accepts_medicare_assignment: Optional[str] = Field(None, alias="acceptsMedicareAssignment")
    has_measures: Optional[bool] = Field(None, alias="hasMeasures")
    has_facility_measures: Optional[bool] = Field(None, alias="hasFacilityMeasures")
    has_updated_phone: Optional[bool] = Field(None, alias="hasUpdatedPhone")
    is_duplicate_address: Optional[bool] = Field(None, alias="isDuplicateAddress")
    is_canonical_address: Optional[bool] = Field(None, alias="isCanonicalAddress")
    specialties: Optional[List[Specialty]] = None
    group_affiliations: Optional[List] = Field(None, alias="groupAffiliations")
    board_certifications: Optional[BoardCertifications] = None
    class Config:
        extra = "allow"


class ProviderInfo(BaseModel):
    """Provider information."""
    distance: Optional[float] = None
    name: Optional[str] = None
    id: Optional[str] = None
    type: Optional[str] = None
    provider_id: Optional[str] = Field(None, alias="providerId")
    sort_name: Optional[str] = Field(None, alias="sortName")
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    address_state: Optional[str] = Field(None, alias="addressState")
    is_duplicate_address: Optional[bool] = Field(None, alias="isDuplicateAddress")
    is_canonical_address: Optional[bool] = Field(None, alias="isCanonicalAddress")
    sort_name_alt: Optional[str] = Field(None, alias="sort_name")
    physician: Optional[Physician] = None
    class Config:
        extra = "allow"


class ProviderRecommendations(BaseModel):
    provider_infos: Optional[List[ProviderInfo]] = None
    specialty: Optional[str] = None
    reasoning: Optional[str] = None
    confidence: Optional[str] = None


class ProviderConfirmationInfo(BaseModel):
    """Provider confirmation information after connecting."""
    provider_id: Optional[str] = None
    provider_name: Optional[str] = None
    confirmation_code: Optional[str] = None
    status: Optional[str] = None
    contact_info: Optional[Dict] = None
    additional_info: Optional[Dict] = None


class PatientInfo(BaseModel):
    """Patient information."""
    name: Optional[str] = None
    date_of_birth: Optional[str] = Field(None, alias="dateOfBirth")
    policy_num: Optional[str] = Field(None, alias="policyNum")
    insurance_company: Optional[str] = Field(None, alias="insuranceCompany")
    date_time_range: Optional[str] = Field(None, alias="dateTimeRange")