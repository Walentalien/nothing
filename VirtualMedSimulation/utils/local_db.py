"""
Local SQLite database configuration for VirtualDoctor
"""
import os
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.database_models import Base, Patient, TestResult, ImagingResult, TreatmentRecord, Doctor, MedicalCondition, User, GameProgress, Medication, MedicationRecord

# Create a SQLite database in the project directory
DATABASE_URL = "sqlite:///virtualdoctor.db"

# Create SQLite engine
engine = create_engine(DATABASE_URL)

# Create session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def init_db():
    """Initialize the database tables"""
    try:
        # Create all tables
        Base.metadata.create_all(engine)
        print("SQLite database initialized with all tables")
    except Exception as e:
        print(f"Error initializing SQLite database: {e}")

# Initialize the database when this module is imported
init_db()