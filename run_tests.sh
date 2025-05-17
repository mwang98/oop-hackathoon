#!/bin/bash
# Run all tests using pytest

# Activate virtual environment
source venv/bin/activate

# Run tests with pytest
pytest tests/ -v

# Output test coverage report
# Uncomment this line if you install pytest-cov package
# pytest tests/ --cov=app --cov-report=term-missing
