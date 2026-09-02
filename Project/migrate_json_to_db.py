"""
One-time script to copy data from your existing patients.json
into the new SQLAlchemy-backed patients.db.
"""
import json
from database import SessionLocal, engine, Base
import db_models

Base.metadata.create_all(bind=engine)

with open("patients.json", "r") as f:
    data = json.load(f)

db = SessionLocal()
try:
    for patient_id, info in data.items():
        exists = db.query(db_models.PatientDB).filter(db_models.PatientDB.id == patient_id).first()
        if exists:
            print(f"Skipping {patient_id}, already in DB")
            continue

        db_patient = db_models.PatientDB(
            id=patient_id,
            name=info["name"],
            city=info.get("city", "Unknown"),
            age=info["age"],
            gender=info["gender"].strip().lower(),
            height=info["height"],
            weight=info["weight"],
        )
        db.add(db_patient)
        print(f"Migrated {patient_id}")

    db.commit()
finally:
    db.close()

print("Migration complete.")
