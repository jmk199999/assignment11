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

from app.models.calculation import Calculation
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
    
