# ======================================================================================
# tests/integration/test_user.py
# ======================================================================================
# Purpose: Demonstrate user model interactions with the database using pytest fixtures.
#          Relies on 'conftest.py' for database session management and test isolation.
# ======================================================================================

import pytest
import logging
import uuid
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.models.calculation import Calculation, Addition, Subtraction, Multiplication, Division
from app.models.user import User
from tests.conftest import create_fake_user, managed_db_session

# Use the logger configured in conftest.py
logger = logging.getLogger(__name__)

# Helper function to create a dummy user_id for testing.
def dummy_user_id():
    return uuid.uuid4()

def test_database_connection(db_session):
    """
    Verify that the database connection is working.
    
    Uses the db_session fixture from conftest.py, which truncates tables after each test.
    """
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1
    logger.info("Database connection test passed")

# ======================================================================================
# Test calculation recording & Partial Commits
# ======================================================================================

def test_calculation_recording(db_session):
    """
    Demonstrate partial commits:
      - user1 is committed
      - user2 fails (duplicate email), triggers rollback, user1 remains
      - user3 is committed
      - final check ensures we only have user1 and user3
    """
    initial_count = db_session.query(Calculation).count()
    logger.info(f"Initial calculation count before test_calculation_recording: {initial_count}")
    assert initial_count == 0, f"Expected 0 calculations before test, found {initial_count}"
    
    user_id = dummy_user_id()
    user = User(
        id = user_id,
        first_name="Dummy",
        last_name="User",
        email="duser@njit.edu",
        username = "Dummy_User",
        password="hashed_password"
    )
    db_session.add(user)
    db_session.commit()

    calc = Calculation(
        user_id = user_id,
        type = "Addition",
        a = 1,
        b = 2
    )

    db_session.add(calc)
    db_session.commit()

    new_count = db_session.query(Calculation).count()
    logger.info(f"Updated calculation count after test_calculation_recording: {new_count}")
    assert new_count == 1, f"Expected 1 calculation after test, found {new_count}"


def test_factory_invalid_type():
    """
    Test factory returns error if unrecognized operation
    """
    with pytest.raises(ValueError, match="Unsupported calculation type: power"):
        calc = Calculation.create(
            calculation_type='power', 
            user_id = dummy_user_id(),
            a = 12,
            b = 13
        )

# ADDITION TESTS

def test_addition():
    """
    Test Addition.get_result
    """
    a = 10
    b = 8.5
    addition = Addition(user_id=dummy_user_id(), a=a, b=b)
    result = addition.get_result()
    assert result == (a+b), f"Expected {(a+b)}, got {result}"

def test_addition_factory():
    """
    Test Addition factory
    """
    a = 10
    b = 8.5
    calc = Calculation.create(
        calculation_type='AdDiTiOn', 
        user_id = dummy_user_id(),
        a = a,
        b = b
    )

    assert isinstance(calc, Addition), "Factory did not return an Addition instance"
    result = calc.get_result()
    assert result == (a+b), f"Expected {(a+b)}, got {result}"

# SUBTRACTION TESTS

def test_subtraction():
    """
    Test Subtraction.get_result
    """
    a = 10
    b = 8.5
    subtraction = Subtraction(user_id=dummy_user_id(), a=a, b=b)
    result = subtraction.get_result()
    assert result == (a-b), f"Expected {(a+b)}, got {result}"

def test_subtraction_factory():
    """
    Test Subtraction factory
    """
    a = 10
    b = 8.5
    calc = Calculation.create(
        calculation_type='Subtraction', 
        user_id = dummy_user_id(),
        a = a,
        b = b
    )

    assert isinstance(calc, Subtraction), "Factory did not return an Subtraction instance"
    result = calc.get_result()
    assert result == (a-b), f"Expected {(a-b)}, got {result}"

# MULTIPLICATION TESTS

def test_multiplication():
    """
    Test Multiplication.get_result
    """
    a = 10
    b = 8.5
    multiplication = Multiplication(user_id=dummy_user_id(), a=a, b=b)
    result = multiplication.get_result()
    assert result == (a*b), f"Expected {(a*b)}, got {result}"

def test_multiplication_factory():
    """
    Test Multiplication factory
    """
    a = 10
    b = 8.5
    calc = Calculation.create(
        calculation_type='Multiplication', 
        user_id = dummy_user_id(),
        a = a,
        b = b
    )

    assert isinstance(calc, Multiplication), "Factory did not return an Multiplication instance"
    result = calc.get_result()
    assert result == (a*b), f"Expected {(a*b)}, got {result}"

# DIVISION TESTS

def test_division():
    """
    Test Division.get_result
    """
    a = 10
    b = 8.5
    division = Division(user_id=dummy_user_id(), a=a, b=b)
    result = division.get_result()
    assert result == (a/b), f"Expected {(a/b)}, got {result}"

def test_division_factory():
    """
    Test Division factory
    """
    a = 10
    b = 8.5
    calc = Calculation.create(
        calculation_type='Division', 
        user_id = dummy_user_id(),
        a = a,
        b = b
    )

    assert isinstance(calc, Division), "Factory did not return an Division instance"
    result = calc.get_result()
    assert result == (a/b), f"Expected {(a/b)}, got {result}"

def test_division_by_zero():
    """
    Test Division by zero
    """
    a = 10
    b = 0
    division = Division(user_id=dummy_user_id(), a=a, b=b)
    with pytest.raises(ValueError, match="Division by zero not permitted."):
        division.get_result()


