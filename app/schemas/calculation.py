from pydantic import BaseModel, Field, ConfigDict, model_validator, field_validator
from enum import Enum
from uuid import UUID


class CalculationType(str, Enum):
    """ For Validating Type """
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"

class CalculationBase(BaseModel):
    """Base calculation schema with common fields"""
    type: str = Field(max_length=50, example="Add")
    a: float = Field(example=3)
    b: float = Field(example=4)

    model_config = ConfigDict(from_attributes=True)

    @field_validator("type", mode="before")
    @classmethod
    def check_type_is_valid(cls, v):
        allowed = {i.value for i in CalculationType}
        if not isinstance(v, str):
            raise ValueError("Type must be a string")
        if v.lower() not in allowed:
            raise ValueError("Type must be 'add', 'subtract', 'multiply' or 'divide'")
        return v.lower()

    @field_validator("a", mode="before")
    @classmethod
    def check_a_is_number(cls, v):
        if not isinstance(v, int) and not isinstance(v, float):
            raise ValueError("First value should be a number")
        return v

    @field_validator("b", mode="before")
    @classmethod
    def check_b_is_number(cls, v):
        if not isinstance(v, int) and not isinstance(v, float):
            raise ValueError("Second value should be a number")
        return v

    @model_validator(mode="after")
    def check_div_by_zero(self) -> "CalculationBase":
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Cannot divide by zero")
        return self

class CalculationCreate(CalculationBase):
    """Schema for creating a new Calculation"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "Add",
                "a": 3,
                "b": 2
            }
        }
    )

class CalculationUpdate(BaseModel):
    """Schema for updating an existing Calculation"""
    a: float = Field(
        None,
        description="Updated First value for caluclation",
        example=2
    )

    b: float = Field(
        None,
        description="Updated Second value for caluclation",
        example=2
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"a": 4, "b": 3}}
    )

class CalculationResponse(CalculationBase):
    """Schema for reading a Calculation from the database"""
    id: UUID = Field(
        ...,
        description="Unique UUID of the calculation",
        example="123e4567-e89b-12d3-a456-426614174999"
    )
    type: str = Field(
        ...,
        description="Type of calculation",
        example="Add"
    )
    a: float = Field(..., description="First Value", example=9)
    b: float = Field(..., description="Second value", example=8)
    result: float = Field(
        ...,
        description="Result of the calculation",
        example=17
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174999",
                "type": "add",
                "a": 9,
                "b": 8,
                "result": 17,
            }
        }
    )
