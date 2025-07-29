from datetime import datetime
import uuid

from sqlalchemy import Column, ForeignKey, String, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from app.database import Base
from app.models.user import User

class Calculation(Base):
    __tablename__ = 'calculations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
#    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    type = Column(String(50), nullable=False)
    inputs = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    #user = relationship("users", back_populates="calculations")

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "calculation",
        "with_polymorphic": "*",
    }

