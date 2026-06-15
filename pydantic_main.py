#Importing library
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Address_model(BaseModel):
    city: str
    state: str
    pincode: str

class Patient(BaseModel):
   
    name: Annotated[str, Field(max_length=50, title='Name of Patient')]
    age: Annotated[int, Field(gt=0, description='Age must not be negative')]
    email: Annotated[EmailStr, Field(description='email of patients')]
    linkedIn_URL: Annotated[Optional[AnyUrl], Field(description='This contains the linkedin profile of patient') ]
    weight: Annotated[float, Field(gt=0)]
    height: float
    allergies: Annotated[Optional[List[str]], Field(default=None, description='Allergies are optional')]
    Contact_details: Annotated[Optional[Dict[str,str]], Field(description='Contains mobile number')]
    Is_married: Annotated[bool, Field(default=False)]
    Address: Address_model

    #Field validation on one field
    @field_validator('email', mode='after')
    @classmethod
    def email_validator(cls, value):
        valid_email_domain = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_email_domain:
            raise ValueError('Not a Valid domain name')
        return value
    

    @field_validator('name', mode='after')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    

    @field_validator('age', mode='after')
    @classmethod
    def age_validator(cls, value):
        if value >10:
            return value
        raise ValueError('Age must be above 10')
    
    #Model validation on more than one field
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.Contact_details:
           raise ValueError('No emergency contact. Please add')
        return model
    
    
    # Compute the bmi from weight and height from user
    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight)/(self.height**2)
        return bmi



#Raw input for adress model
Address_info = {
                'city': 'SFO',
                'state': 'CA',
                'pincode': '123456'
            }

#Object creation of model
address_11 = Address_model(**Address_info)

#raw input for patient
patient_info = {
                'name': 'Nick', 
                'age': '30', 
                'email': 'abc@hdfc.com',
                'linkedIn_URL': 'https://www.linkedin.com/in/neha-gour/',
                'weight': '50', 
                'height': '5',
                'Contact_details':{'phone_number':'916911911', 'emergency': '916911012'}, 
                'Address' : address_11
                }
#Object creation of patients
patient_11 = Patient(**patient_info)

#To convert your progeam inform of library or json
temp = patient_11.model_dump_json()
#temp = patient_11.model_dump_json(include=['name'])
#temp = patient_11.model_dump_json(exclude={'address':['city']})
#temp = patient_11.model_dump_json(exclude_unset=True)

def update_data(patient_1: Patient):
    print("Patients data is updated...")

update_data(patient_11)