import json
from fastapi import FastAPI,Path, HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional

app = FastAPI()

#Pydantic class for data validation
class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the Patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the Patient')]
    city: Annotated[str, Field(..., description='City of the Patient')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the Patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height:Annotated[float, Field(..., gt=0, description='Height in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight in Kgs')]

    #computed field to calculate BMI(depends of ht & wt)
    @computed_field
    @property
    def bmi(self) -> float:
            bmi = round(self.weight/(self.height**2), 2)
            return bmi
    #computed field for verdict(depends on bmi)
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 25:
            return 'normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return ' Obese'


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal["male", "female","others"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

#function to load the json file to access the data all time
def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data
#function to save data(it receives the data as dict and puts in json)
def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)



@app.get("/")
async def home():
    return {"message": "Patient Management System"}

@app.get("/about")
async def about():
    return {"message": "About Section of Patient management"}

@app.get("/view")
async def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
async def view_patient(patient_id: str = Path(..., description= 'ID of the patient', examples='P001')):
    #load all the patients
    data = load_data()

    #Check if id exists return that else error
    if patient_id in data:
        return data[patient_id]
    # return{"ERROR!": "No data found"}
    raise HTTPException(status_code=404, detail='Patient not found')

#Query parameters
@app.get('/sort')
async def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height_cm, weight_kg, gender or bmi'), 
order: str = Query('asc', description='Sort in asc or desc order')):
    #Assign a variable
    valid_fields = ['height', 'weight', 'bmi', 'gender']

    #Error handling
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='Invalid order select asc or desc  ')

    data = load_data()
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by,0 ), reverse = sort_order)
    return sorted_data

#POST request to insert data to patients.json
@app.post('/create')
async def create_patient(patient: Patient):
    #load the data
    data = load_data()
    #Check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')
    #new patient add to the database(converting pydantic object to dict as existing data is dict while model is pydantic object)
    data[patient.id] = patient.model_dump(exclude=['id']) #exclude id as key is id and the values are rest fields

    # save the data using utility function defined above
    save_data(data)

    #return json response
    return JSONResponse(status_code= 201, content={'message': 'Patient created Successfully'})


#PUT request to edit data 
@app.put('/edit/{patient_id}')
async def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    #Check if patient exits
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    #extract the data by patient id
    existing_patient_info = data[patient_id] #All data

    #get the user values frompatient update and modify the existing data
    #convert the pydantic object to dict
    updated_patient_info = patient_update.model_dump(exclude_unset=True) #only convert the provided data to dict

    #loop in provided key and values and put them in existing
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #Issue:BMI and verdict is not calculated based on new data
    #Sol: existing_patient_info -> pydantic object -> updated bmi , verdict
    existing_patient_info['id'] = patient_id # get the id before converting
    patient_pydantic_obj = Patient(**existing_patient_info)
    #-> Pydantic obj -> dict
    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    #add this dict to data
    data[patient_id] = existing_patient_info

    #save data
    save_data(data)

    #Success
    return JSONResponse(status_code=200, content={'message':'Patient updated successfully'})

#Delete request to delete data
@app.delete('/delete/{patient_id}')
async def delete_patient(patient_id: str):
    #load data
    data = load_data()

    #Check if id exists else show error
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]

    #save data
    save_data(data)

    #Success
    return JSONResponse(status_code=200, content={'message':'patient deleted successfully'})

