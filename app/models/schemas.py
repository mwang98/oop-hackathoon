"""
Schema definitions for provider finder application.
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class Location(BaseModel):
    """Location information with latitude and longitude."""
    latitude: float
    longitude: float


class Specialty(BaseModel):
    """Detailed specialty information."""
    id: str
    specialty_name: str = Field(..., alias="specialtyName")
    specialty_id: Optional[str] = Field(None, alias="specialtyId")
    description: Optional[str] = None
    exclude: bool = False
    physician_specialty: Optional[Dict] = Field(None, alias="physicianSpecialty")


class BoardCertification(BaseModel):
    """Board certification information."""
    name: str
    source: str


class BoardCertifications(BaseModel):
    """Collection of board certifications."""
    board_certifications: List[BoardCertification] = Field(..., alias="boardCertifications")


class Physician(BaseModel):
    """Detailed physician information."""
    name: str
    date_imported: str = Field(..., alias="dateImported")
    hash: str
    id: str
    provider_id: str = Field(..., alias="providerId")
    address_line1: str = Field(..., alias="addressLine1")
    address_city: str = Field(..., alias="addressCity")
    address_state: str = Field(..., alias="addressState")
    address_zipcode: str = Field(..., alias="addressZipcode")
    phone: Optional[str] = None
    geocode_source: str = Field(..., alias="geocodeSource")
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    middle_name: Optional[str] = Field(None, alias="middleName")
    suffix: Optional[str] = None
    gender: str
    credential: str
    medical_school_name: str = Field(..., alias="medicalSchoolName")
    graduation_year: str = Field(..., alias="graduationYear")
    telehealth: bool
    organization_name: Optional[str] = Field(None, alias="organizationName")
    pac_id: str = Field(..., alias="pacId")
    group_practice_pac_id: Optional[str] = Field(None, alias="groupPracticePacId")
    group_accepts_medicare_assignment: bool = Field(..., alias="groupAcceptsMedicareAssignment")
    address_line2: Optional[str] = Field(None, alias="addressLine2")
    address_id: str = Field(..., alias="addressId")
    address_line2_suppress: bool = Field(..., alias="addressLine2suppress")
    accepts_medicare_assignment: str = Field(..., alias="acceptsMedicareAssignment")
    has_measures: bool = Field(..., alias="hasMeasures")
    has_facility_measures: bool = Field(..., alias="hasFacilityMeasures")
    has_updated_phone: bool = Field(..., alias="hasUpdatedPhone")
    is_duplicate_address: bool = Field(..., alias="isDuplicateAddress")
    is_canonical_address: bool = Field(..., alias="isCanonicalAddress")
    specialties: List[Specialty]
    group_affiliations: List = Field(..., alias="groupAffiliations")
    board_certifications: BoardCertifications
    class Config:
        extra = "allow"


class ProviderInfo(BaseModel):
    """Provider information."""
    distance: float
    name: str
    id: str
    type: str
    provider_id: str = Field(..., alias="providerId")
    sort_name: str = Field(..., alias="sortName")
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    address_state: str = Field(..., alias="addressState")
    is_duplicate_address: bool = Field(..., alias="isDuplicateAddress")
    is_canonical_address: bool = Field(..., alias="isCanonicalAddress")
    sort_name_alt: str = Field(..., alias="sort_name")
    physician: Physician
    class Config:
        extra = "allow"


class ProviderConfirmationInfo(BaseModel):
    """Provider confirmation information after connecting."""
    provider_id: str
    provider_name: str
    confirmation_code: str
    status: str
    contact_info: Dict
    additional_info: Optional[Dict] = None
