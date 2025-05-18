from app.models.schemas import (
    ProviderInfo,
    ProviderRecommendations,
)

DEFAULT_PROVIDER_RECOMMENDATIONS = [
    ProviderRecommendations(
        provider_infos=[
            ProviderInfo(
                id="12345",
                name="Dr. Nikhil Krishnan",
                type="Physician",
                distance=5.0,
                address_state="CA",
                sort_name="Krishnan, Nikhil",
                first_name="Nikhil",
                last_name="Krishnan",
                is_duplicate_address=False,
                is_canonical_address=True,
            )
        ],
        specialty="Internal Medicine",
        reasoning="Based on your symptoms and location.",
        confidence="High",
    ),
    ProviderRecommendations(
        provider_infos=[
            ProviderInfo(
                id="12345",
                name="Dr. Jonathan Doe",
                type="Physician",
                distance=5.0,
                address_state="CA",
                sort_name="Doe, Jonathan",
                first_name="Jonathan",
                last_name="Doe",
                is_duplicate_address=False,
                is_canonical_address=True,
            )
        ],
        specialty="Internal Medicine",
        reasoning="Based on your symptoms and location.",
        confidence="High",
    ),
]
