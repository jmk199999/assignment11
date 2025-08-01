import pytest
from pydantic import ValidationError
from uuid import uuid4
from datetime import datetime
from app.schemas.calculation import (
    CalculationCreate,
    CalculationUpdate,
    CalculationResponse
)

def test_calculation_create_valid():
    """Test creating a valid CalculationCreate schema."""
    data = {
        "type": "subtract",
        "a": 10,
        "b": 6
    }
    calc = CalculationCreate(**data)
    assert calc.type == "subtract"
    assert calc.a == 10
    assert calc.b == 6

def test_calculation_type_string():
    """Test invalid type."""
    data = {
        "type": 13,
        "a": 4,
        "b": 5
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    # Look for a substring that indicates a missing required field.
    assert "must be a string" in str(exc_info.value).lower()

def test_calculation_type_valid():
    """Test invalid type."""
    data = {
        "type": "invalid",
        "a": 4,
        "b": 5
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    # Look for a substring that indicates a missing required field.
    assert "must be 'add'" in str(exc_info.value).lower()

def test_calculation_a_valid():
    """Test invalid a."""
    data = {
        "type": "add",
        "a": "four",
        "b": 5
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    # Look for a substring that indicates a missing required field.
    assert "first value should be a number" in str(exc_info.value).lower()

def test_calculation_b_valid():
    """Test invalid b."""
    data = {
        "type": "add",
        "a": 4,
        "b": "five"
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    # Look for a substring that indicates a missing required field.
    assert "second value should be a number" in str(exc_info.value).lower()

def test_calculation_div_zero():
    """Test invalid divide by zero."""
    data = {
        "type": "Divide",
        "a": 4,
        "b": 0
    }
    with pytest.raises(ValidationError) as exc_info:
        CalculationCreate(**data)
    # Look for a substring that indicates a missing required field.
    assert "cannot divide by zero" in str(exc_info.value).lower()

