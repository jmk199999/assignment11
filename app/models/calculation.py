from datetime import datetime
import uuid

from typing import List
from sqlalchemy import Column, ForeignKey, String, JSON, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import  relationship
from sqlalchemy.ext.declarative import declared_attr
from app.database import Base
from app.operations import Number

class AbstractCalculation():
    """ Abstract class for Calculation """
    
#    @declared_attr
#    def __tablename__(cls):
#        return 'calculations'

    @declared_attr
    def id(cls):
        return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,nullable=False)
    
    @declared_attr
    def user_id(cls):
        return Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    @declared_attr
    def type(cls): 
        return Column(String(50), nullable=False, index=True)
    
    @declared_attr
    def a(cls): 
        return Column(Float, nullable=False)
    
    @declared_attr
    def b(cls):
        return Column(Float, nullable=True)

    @declared_attr
    def user(cls): 
        return relationship("User", back_populates="calculations")

    @classmethod
    def create(cls, calculation_type: str, user_id: uuid.UUID, a: Number, b: Number) -> "Calculation":
        """ Factory method for Calculations """
        calculation_classes = {
            'addition': Addition,
            'subtraction': Subtraction,
            'multiplication': Multiplication,
            'division': Division
        }
        calc_class = calculation_classes.get(calculation_type.lower())
        if not calc_class:
            raise ValueError(f"Unsupported calculation type: {calculation_type}")
        return calc_class (user_id=user_id, a=a, b=b)

    def get_result(self) -> float: 
        """Method to compute calculation result"""
        raise NotImplementedError # pragma: no cover

    def __repr__(self):
        return f"<Calculation(type={self.type}, a={self.a}, b={self.b})>" # pragma: no cover


class Calculation(Base, AbstractCalculation):
    """ Base Calculation method """

    __tablename__ = 'calculations'

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "calculation",
        "with_polymorphic": "*",
    }

class Addition(Calculation):
    """ Addition class """
    __mapper_args__ = {"polymorphic_identity": "addition"}

    def get_result(self) -> float:
        return self.a + self.b

class Subtraction(Calculation):
    """ Subtraction class """
    __mapper_args__ = {"polymorphic_identity": "subtraction"}

    def get_result(self) -> float:
        return self.a - self.b

class Multiplication(Calculation):
    """ Multiplication class """
    __mapper_args__ = {"polymorphic_identity": "subtraction"}

    def get_result(self) -> float:
        return self.a * self.b

class Division(Calculation):
    """ Division class """
    __mapper_args__ = {"polymorphic_identity": "division"}

    def get_result(self) -> float:
        if self.b == 0:
            raise ValueError("Division by zero not permitted.") 
        return self.a / self.b
