from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
from fastapi.responses import JSONResponse

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Unique ID of patient')]
    name: Annotated[str, Field(..., max_length=50, description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where patient lives')]
    age: Annotated[int, Field(..., ge=0, lt=100, description='age of the patient' )]
    gender: Annotated[Literal['male', 'female'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., ge=0, description='height of the patient in meters' )]
    weight: Annotated[float, Field(..., ge=0, description='weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self)-> float:
        return round(self.weight/(self.height**2),2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 30:
            return 'Normal'
        else: 
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None,max_length=50, description='Name of the patient')]
    city: Annotated[Optional[str], Field(default=None,description='City where patient lives')]
    age: Annotated[Optional[int], Field(default=None, ge=0, lt=100, description='age of the patient' )]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None, description='Gender of the patient')]
    height: Annotated[Optional[float], Field(default=None, ge=0, description='height of the patient in meters' )]
    weight: Annotated[Optional[float], Field(default=None, ge=0, description='weight of the patient in kgs')]


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        data = json.dump(data,f)
    return data

# Retriving of data 
@app.get('/')
def root():

    return ("This page contains the patients info")

@app.get('/view')
def view():
    #Load and return all data
    data = load_data()
    return data

@app.get('/patients/{patient_id}')
def view_patientS(patient_id: str = Path(..., description='This is the info about patient')):
    #load all data
    data = load_data()

    #Find a patient by its ID
    if patient_id in data:
        return data[patient_id]
    #else:
    #   return{'ERROR: Patient Not Found'}
    raise HTTPException(status_code=404, detail='NOT FOUND')

@app.get('/sort')
def sorted_Patients(sort_by: str = Query(...), 
                    order: str = Query('asc')):

    valid_sort_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, 
                            detail=f'Invalid field select from {valid_sort_fields}')
    
    valid_order_fields =['asc', 'desc']
    if order not in valid_order_fields:
        raise HTTPException(status_code=400, 
                            detail=f'Invalid field select from {valid_order_fields}')
    
    
    data = load_data()
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(),
                        key=lambda x: x.get(sort_by, 0), 
                        reverse=sort_order)

    return sorted_data

#Checking Existing data and creating the new record
@app.post('/create')
def create_function(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    #Converting patient pydantic model into dictonary as our existing data in json
    data[patient.id] = patient.model_dump(exclude=['id'])

    # Now save the above dictionary into json file 
    save_data(data)

    # Now telling the client that the job is done
    return JSONResponse(status_code=200, content={'message': 'Patient added succesfully'})

@app.put('/edit/{patient_id}')
def UpdatePatient(patient_id: str, patientupdate: PatientUpdate):

    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient Not Found')
    
    ExistingInfo = data[patient_id] #all the fields

    #Convert Pydentic Model to Dictonary
    UpdatedInfo = patientupdate.model_dump(exclude_unset=True) # only want to fetch two  what client want to edit, instead of all

    for key , value in UpdatedInfo.items():
        ExistingInfo[key] = value

    #Convert Dictonary to pydantic model
    #ExistingInfo --> into pydantic object --> updated bmi+verdict
    ExistingInfo['id'] = patient_id
    patient_pydantic_object= Patient(**ExistingInfo) 
    #pydantic object into dictionary
    ExistingInfo = patient_pydantic_object.model_dump(exclude='id')

    data[patient_id] = ExistingInfo

    save_data(data)
    return JSONResponse(status_code=200, content={'message': 'Succesfully updated'})


@app.delete('/delete/{patient_id}')
def DeletePatient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient Not Found')
    
    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient deleted succesfully'})