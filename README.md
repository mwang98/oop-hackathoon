# Provider Finder Backend

A Python package for finding and connecting with healthcare providers.

## Installation

### Development Installation

To install the package in development mode:

```bash
# Clone the repository
git clone <repository-url>
cd oop

# Install in development mode
pip install -e .
```

### Regular Installation

To install the package for regular use:

```bash
pip install .
```

## Usage

### Running the API Server

```python
# Method 1: Using the CLI script
python provider_finder_cli.py

# Method 2: Importing the app directly
from app.main import app
import uvicorn

uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Using the Package Components

```python
# Import specific components
from app.utils.llm_client import LLMClient
from app.services.provider_service import ProviderService

# Initialize components
llm_client = LLMClient()
provider_service = ProviderService()

# Use them in your application
# ...
```

See `example_usage.py` for a complete usage example.

## Project Structure

### Core Modules

#### 1. Provider Recommendation
- Input: Zip code
- Output: List[ProviderInfo]

#### 2. Provider Connection
- Input: List[ProviderInfo]
- Output: List[ProviderConfirmationInfo]

### Helper Functions

#### 1. Geolocation
- Input: Zip code
- Output: Latitude/Longitude

#### 2. Provider Search
- Input: Latitude/Longitude, Radius
- Output: List[ProviderInfo]

#### 3. Symptom Matching
- Input: Symptoms
- Output: List[ProviderSpecialty]

## Development

### Testing

```bash
# Run all tests
pytest

# Run specific tests
pytest tests/test_provider_service.py
```
