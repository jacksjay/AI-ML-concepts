from fastapi import FastAPI, Depends, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import db_models
import schemas
import crud
from database import engine, get_db

# Creates the patients table (and patients.db file) if they don't exist yet.
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Patient Management System (SQLAlchemy)")

VALID_SORT_FIELDS = ['height', 'weight', 'age', 'gender']


@app.get("/")
async def home():
    return {"message": "Patient Management System (DB-backed)"}


@app.get("/view", response_model=list[schemas.PatientResponse])
async def view_all(db: Session = Depends(get_db)):
    return crud.get_all_patients(db)


@app.get("/patient/{patient_id}", response_model=schemas.PatientResponse)
async def view_patient(
    patient_id: str = Path(..., description='ID of the patient', examples=['P001']),
    db: Session = Depends(get_db),
):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail='Patient not found')
    return patient


@app.get("/sort", response_model=list[schemas.PatientResponse])
async def sort_patients(
    sort_by: str = Query(..., description=f'Sort on the basis of {VALID_SORT_FIELDS}'),
    order: str = Query('asc', description='Sort in asc or desc order'),
    db: Session = Depends(get_db),
):
    if sort_by not in VALID_SORT_FIELDS:
        raise HTTPException(status_code=400, detail=f'Invalid field, select from {VALID_SORT_FIELDS}')
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order, select asc or desc')

    return crud.get_sorted_patients(db, sort_by, order)


@app.post("/create", status_code=201)
async def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    existing = crud.get_patient(db, patient.id)
    if existing:
        raise HTTPException(status_code=400, detail='Patient already exists')

    crud.create_patient(db, patient)
    return JSONResponse(status_code=201, content={'message': 'Patient created successfully'})


@app.put("/edit/{patient_id}")
async def update_patient(
    patient_id: str,
    patient_update: schemas.PatientUpdate,
    db: Session = Depends(get_db),
):
    updated = crud.update_patient(db, patient_id, patient_update)
    if not updated:
        raise HTTPException(status_code=404, detail='Patient not found')
    return JSONResponse(status_code=200, content={'message': 'Patient updated successfully'})


@app.delete("/delete/{patient_id}")
async def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_patient(db, patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Patient not found')
    return JSONResponse(status_code=200, content={'message': 'Patient deleted successfully'})
