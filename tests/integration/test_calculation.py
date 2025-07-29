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

    inputs = [1, 2, 3]
    calc = Calculation(
        user_id = user_id,
        type = "Addition",
        inputs = inputs
    )

    db_session.add(calc)
    db_session.commit()

def test_factory_invalid_type():
    """
    Test factory returns error if unrecognized operation
    """
    inputs = [12, 13]
    with pytest.raises(ValueError, match="Unsupported calculation type: power"):
        calc = Calculation.create(
            calculation_type='power', 
            user_id = dummy_user_id(),
            inputs=inputs
        )

# ADDITION TESTS

def test_addition():
    """
    Test Addition.get_result
    """
    inputs = [10, 5, 3.5]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    result = addition.get_result()
    assert result == sum(inputs), f"Expected {sum(inputs)}, got {result}"

def test_addition_factory():
    """
    Test Addition factory
    """
    inputs = [12, 10, 9, 18, -30]
    calc = Calculation.create(
        calculation_type='AdDiTiOn', 
        user_id = dummy_user_id(),
        inputs=inputs
    )

    assert isinstance(calc, Addition), "Factory did not return an Addition instance"
    result = calc.get_result()
    assert result == sum(inputs), f"Expected {sum(inputs)}, got {result}"

def test_addition_one_input():
    """
    Test Addition with one factor generates error message
    """
    inputs = [10]
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        addition.get_result()

def test_addition_invalid_input():
    """
    Test Addition with one factor generates error message
    """
    inputs = "12 + 13"
    addition = Addition(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        addition.get_result()

# SUBTRACTION TESTS

def test_subtraction():
    """
    Test Subtraction.get_result
    """
    inputs = [10, 5, 3.5]
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=inputs)
    result = subtraction.get_result()
    assert result == 1.5, f"Expected 1.5, got {result}"

def test_subtraction_factory():
    """
    Test Subtraction factory
    """
    inputs = [10, 5, 3.5]
    calc = Calculation.create(
        calculation_type='Subtraction', 
        user_id = dummy_user_id(),
        inputs=inputs
    )

    assert isinstance(calc, Subtraction), "Factory did not return an Subtraction instance"
    result = calc.get_result()
    assert result == 1.5, f"Expected 1.5, got {result}"

def test_subtraction_one_input():
    """
    Test Subtraction with one factor generates error message
    """
    inputs = [10]
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        subtraction.get_result()

def test_subtraction_invalid_input():
    """
    Test Subtraction with one factor generates error message
    """
    inputs = "12 - 13"
    subtraction = Subtraction(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        subtraction.get_result()

# MULTIPLICATION TESTS

def test_multiplication():
    """
    Test Multiplication.get_result
    """
    inputs = [1, 2, 3]
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=inputs)
    result = multiplication.get_result()
    assert result == 6, f"Expected 6, got {result}"

def test_multiplication_factory():
    """
    Test Multiplication factory
    """
    inputs = [1, 2, 3]
    calc = Calculation.create(
        calculation_type='Multiplication', 
        user_id = dummy_user_id(),
        inputs=inputs
    )

    assert isinstance(calc, Multiplication), "Factory did not return an Multiplication instance"
    result = calc.get_result()
    assert result == 6, f"Expected 6, got {result}"

def test_multiplication_one_input():
    """
    Test Multiplication with one factor generates error message
    """
    inputs = [10]
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        multiplication.get_result()

def test_multiplication_invalid_input():
    """
    Test Multiplication with one factor generates error message
    """
    inputs = "2 * 3"
    multiplication = Multiplication(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        multiplication.get_result()

# DIVISION TESTS

def test_division():
    """
    Test Division.get_result
    """
    inputs = [42, 3, 2]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    result = division.get_result()
    assert result == 7, f"Expected 7, got {result}"

def test_division_factory():
    """
    Test Division factory
    """
    inputs = [42, 3, 2]
    calc = Calculation.create(
        calculation_type='Division', 
        user_id = dummy_user_id(),
        inputs=inputs
    )

    assert isinstance(calc, Division), "Factory did not return an Division instance"
    result = calc.get_result()
    assert result == 7, f"Expected 7, got {result}"

def test_division_one_input():
    """
    Test Division with one factor generates error message
    """
    inputs = [10]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Inputs must be a list with at least two numbers."):
        division.get_result()

def test_division_invalid_input():
    """
    Test Division with one factor generates error message
    """
    inputs = "12 / 13"
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Inputs must be a list of numbers."):
        division.get_result()

def test_division_by_zero():
    """
    Test Division by zero
    """
    inputs = [42, 2, 3, 0]
    division = Division(user_id=dummy_user_id(), inputs=inputs)
    with pytest.raises(ValueError, match="Division by zero not permitted."):
        division.get_result()


