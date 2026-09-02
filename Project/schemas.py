from pydantic import BaseModel, Field, computed_field, field_validator, ConfigDict
from typing import Annotated, Literal, Optional


class PatientBase(BaseModel):
    name: Annotated[str, Field(..., description='Name of the Patient')]
    city: Annotated[str, Field(..., description='City of the Patient')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the Patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight in Kgs')]

    @field_validator('gender', mode='before')
    @classmethod
    def normalize_gender(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v


#Input Schema
# Used for POST /create (id supplied by the client, becomes the primary key)
class PatientCreate(PatientBase):
    id: Annotated[str, Field(..., description='ID of the Patient', examples=['P001'])]


# Used for PUT /edit/{id} 
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

    @field_validator('gender', mode='before')
    @classmethod
    def normalize_gender(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v


# Output Schema 

class PatientResponse(PatientBase):
    #This tells Pydantic to read data directly from the SQLAlchemy ORM object
    model_config = ConfigDict(from_attributes=True) # (from_attributes=True lets Pydantic pull fields off a PatientDB instance)
    id: str

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 25:
            return 'normal'
        elif self.bmi < 30:
            return 'overweight'
        else:
            return 'obese'
