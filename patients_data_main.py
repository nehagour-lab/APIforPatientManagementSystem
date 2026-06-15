from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():

    with open("patients.json", "r") as f:
        data = json.load(f)

    return data

@app.get('/')
def root():

    return ("This page contains the patients info")

@app.get('/view')
def view():
    #Load and return all data
    data = load_data()
    return data

@app.get('/patients/{patient_id}')

#def view_patients(patient_id: str):
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







    
