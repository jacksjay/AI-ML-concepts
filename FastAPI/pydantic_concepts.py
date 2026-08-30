from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional

class Patient(BaseModel):
    name: str = Field(max_length= 50)
    email: EmailStr #builtin pydantic function for email validation
    age: int = Field(gt=0, lt=120 ) # Range for custom data validations 
    height: float
    weight: float = Field(gt=0)
    #Which are not compulsory add optional with defined value as None if not provided
    married: Optional[bool] = None
    allergies: Optional[List[str]] = None
    contact_details: Optional[Dict[str, str]] = None

    #Fied validator on email of hdfc or icic only
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        Valid_domains = ['hdfc.com', 'icici.com']
        #eg abc@gmail.com
        domain_name = value.split('@')[-1] #it spilts the data from @ and we take the end part i.e., [-1]
        #logic
        if domain_name not in Valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    #FieldValidator for capitalise name
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper

#   Model validator: validations depends on more than 1 field
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        #Check for age and emergency keyword in contact details
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have emergency contact')
        return model

    #Computed field: Any field value which can be fetched by other fiedls
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi




def Patient_info(patient: Patient):
    print(patient.name)
    print(patient.age)
    print('BMI', patient.bmi)
    print('Values Inserted')

patient_info =  {'name': 'Nitish', 'email': 'abc@icici.com','age': '30', 'weight': 75.2, 'married':True, 'height': '1.74',
'allergies':['pollen', 'dust'], 'contact_details':{'email':'abc@gmail.com', 'phone':'2353462'}}
#The ** operator in Python is used to unpack a dictionary into keyword arguments when calling a function or creating an object.
patient1 = Patient(**patient_info)
#Call the function
Patient_info(patient1)