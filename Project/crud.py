from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
import db_models
import schemas


def get_patient(db: Session, patient_id: str):
    # Query: "Select * from patients where id == patient_id limit 1"
    return db.query(db_models.PatientDB).filter(db_models.PatientDB.id == patient_id).first()


def get_all_patients(db: Session):
    #"Select * from patients"
    return db.query(db_models.PatientDB).all()


def get_sorted_patients(db: Session, sort_by: str, order: str):
    # getattr grabs the specific column dynamically (e.g., db_models.PatientDB.height)
    column = getattr(db_models.PatientDB, sort_by)
    direction = desc(column) if order == 'desc' else asc(column)
    return db.query(db_models.PatientDB).order_by(direction).all()


def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = db_models.PatientDB(**patient.model_dump()) # patient.model_dump() converts the Pydantic object into a Python dictionary.
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(db: Session, patient_id: str, patient_update: schemas.PatientUpdate):
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None

    update_data = patient_update.model_dump(exclude_unset=True)
    # Loop through provided fields and use setattr to update the database object dynamically
    for key, value in update_data.items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: str):
    db_patient = get_patient(db, patient_id)
    if not db_patient:
        return None
    db.delete(db_patient) #Mark for deletion
    db.commit() #Execute deletion
    return db_patient
