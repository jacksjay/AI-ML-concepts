from sqlalchemy import Column, String, Integer, Float
from database import Base

#PatientDB inherits from Base, telling SQLAlchemy to map this class to a real SQL table
class PatientDB(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    height = Column(Float, nullable=False)  # meters
    weight = Column(Float, nullable=False)  # kg

