"""
PostgreSQL database models for VirtualDoctor
This module defines the SQLAlchemy models for the database.
"""

import os
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Patient(Base):
    """Database model for patients"""
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(20), nullable=False)
    medical_history = Column(Text)  # JSON serialized list
    current_symptoms = Column(Text)  # JSON serialized list
    vital_signs = Column(Text)  # JSON serialized object
    diagnosis = Column(String(100))
    condition_severity = Column(Integer, default=1)
    admission_time = Column(DateTime, default=datetime.now)
    
    # Relationships
    test_results = relationship("TestResult", back_populates="patient", cascade="all, delete-orphan")
    imaging_results = relationship("ImagingResult", back_populates="patient", cascade="all, delete-orphan")
    treatment_records = relationship("TreatmentRecord", back_populates="patient", cascade="all, delete-orphan")
    medication_records = relationship("MedicationRecord", back_populates="patient", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert to dictionary representation"""
        # Convert SQLAlchemy Column values to native Python types
        medical_history = str(self.medical_history) if self.medical_history is not None else None
        current_symptoms = str(self.current_symptoms) if self.current_symptoms is not None else None
        vital_signs = str(self.vital_signs) if self.vital_signs is not None else None
        
        result = {
            'id': self.id,
            'patient_id': self.patient_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'medical_history': json.loads(medical_history) if medical_history else [],
            'current_symptoms': json.loads(current_symptoms) if current_symptoms else [],
            'vital_signs': json.loads(vital_signs) if vital_signs else {},
            'diagnosis': self.diagnosis,
            'condition_severity': self.condition_severity,
            'admission_time': self.admission_time.isoformat() if self.admission_time else None,
        }
        
        # Add relationships if they're initialized
        if hasattr(self, 'test_results') and self.test_results is not None:
            result['test_results'] = [tr.to_dict() for tr in self.test_results]
        if hasattr(self, 'imaging_results') and self.imaging_results is not None:
            result['imaging_results'] = [ir.to_dict() for ir in self.imaging_results]
        if hasattr(self, 'treatment_records') and self.treatment_records is not None:
            result['treatment_records'] = [tr.to_dict() for tr in self.treatment_records]
        if hasattr(self, 'medication_records') and self.medication_records is not None:
            result['medication_records'] = [mr.to_dict() for mr in self.medication_records]
        
        return result
    
    @classmethod
    def from_model(cls, patient):
        """Create a database model from a domain model"""
        vital_signs_dict = {}
        if patient.vital_signs:
            vital_signs_dict = {
                'pulse': patient.vital_signs.pulse,
                'systolic_bp': patient.vital_signs.systolic_bp,
                'diastolic_bp': patient.vital_signs.diastolic_bp,
                'temperature': patient.vital_signs.temperature,
                'respiratory_rate': patient.vital_signs.respiratory_rate,
                'oxygen_saturation': patient.vital_signs.oxygen_saturation
            }
        
        return cls(
            patient_id=patient.patient_id,
            name=patient.name,
            age=patient.age,
            gender=patient.gender,
            medical_history=json.dumps(patient.medical_history),
            current_symptoms=json.dumps(patient.current_symptoms),
            vital_signs=json.dumps(vital_signs_dict),
            diagnosis=patient.diagnosis,
            condition_severity=patient.condition_severity,
            admission_time=patient.admission_time if hasattr(patient, 'admission_time') else datetime.now()
        )


class TestResult(Base):
    """Database model for test results"""
    __tablename__ = 'test_results'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(String(50), ForeignKey('patients.patient_id'), nullable=False)
    test_name = Column(String(100), nullable=False)
    test_time = Column(DateTime, default=datetime.now)
    results = Column(Text)  # JSON serialized test results
    is_abnormal = Column(Boolean, default=False)
    
    # Relationships
    patient = relationship("Patient", back_populates="test_results")
    
    def to_dict(self):
        """Convert to dictionary representation"""
        results_str = str(self.results) if self.results is not None else None
        test_time_obj = self.test_time
        
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'test_name': self.test_name,
            'test_time': test_time_obj.isoformat() if test_time_obj else None,
            'results': json.loads(results_str) if results_str else {},
            'is_abnormal': bool(self.is_abnormal)
        }


class ImagingResult(Base):
    """Database model for imaging results"""
    __tablename__ = 'imaging_results'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(String(50), ForeignKey('patients.patient_id'), nullable=False)
    image_type = Column(String(50), nullable=False)  # X-ray, ECG, etc.
    image_path = Column(String(255), nullable=False)
    description = Column(Text)
    test_time = Column(DateTime, default=datetime.now)
    
    # Relationships
    patient = relationship("Patient", back_populates="imaging_results")
    
    def to_dict(self):
        """Convert to dictionary representation"""
        test_time_obj = self.test_time
        
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'image_type': self.image_type,
            'image_path': self.image_path,
            'description': self.description,
            'test_time': test_time_obj.isoformat() if test_time_obj else None
        }


class TreatmentRecord(Base):
    """Database model for treatment records"""
    __tablename__ = 'treatment_records'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(String(50), ForeignKey('patients.patient_id'), nullable=False)
    treatment_name = Column(String(100), nullable=False)
    treatment_time = Column(DateTime, default=datetime.now)
    effects = Column(Text)  # JSON serialized effects
    vital_changes = Column(Text)  # JSON serialized vital changes
    
    # Relationships
    patient = relationship("Patient", back_populates="treatment_records")
    
    def to_dict(self):
        """Convert to dictionary representation"""
        treatment_time_obj = self.treatment_time
        effects_str = str(self.effects) if self.effects is not None else None
        vital_changes_str = str(self.vital_changes) if self.vital_changes is not None else None
        
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'treatment_name': self.treatment_name,
            'treatment_time': treatment_time_obj.isoformat() if treatment_time_obj else None,
            'effects': json.loads(effects_str) if effects_str else [],
            'vital_changes': json.loads(vital_changes_str) if vital_changes_str else {}
        }


class Doctor(Base):
    """Database model for doctors"""
    __tablename__ = 'doctors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    experience = Column(Integer, default=1)
    patients_treated = Column(Integer, default=0)
    successful_diagnoses = Column(Integer, default=0)
    score = Column(Integer, default=0)
    
    def to_dict(self):
        """Convert to dictionary representation"""
        return {
            'id': self.id,
            'name': self.name,
            'specialization': self.specialization,
            'experience': self.experience,
            'patients_treated': self.patients_treated,
            'successful_diagnoses': self.successful_diagnoses,
            'score': self.score
        }


class MedicalCondition(Base):
    """Database model for medical conditions/diseases"""
    __tablename__ = 'medical_conditions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    symptoms = Column(Text)  # JSON serialized list
    recommended_tests = Column(Text)  # JSON serialized list
    recommended_treatments = Column(Text)  # JSON serialized list
    severity = Column(Integer, default=3)
    
    def to_dict(self):
        """Convert to dictionary representation"""
        symptoms_str = str(self.symptoms) if self.symptoms is not None else None
        tests_str = str(self.recommended_tests) if self.recommended_tests is not None else None
        treatments_str = str(self.recommended_treatments) if self.recommended_treatments is not None else None
        
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'symptoms': json.loads(symptoms_str) if symptoms_str else [],
            'recommended_tests': json.loads(tests_str) if tests_str else [],
            'recommended_treatments': json.loads(treatments_str) if treatments_str else [],
            'severity': self.severity
        }


class User(Base):
    """Database model for user accounts"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    game_progress = relationship("GameProgress", back_populates="user", cascade="all, delete-orphan")
    doctors = relationship("Doctor", secondary="user_doctors", backref="users")
    
    def set_password(self, password):
        """Set the password hash from a plain text password"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary representation (without sensitive data)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }


class GameProgress(Base):
    """Database model for tracking user game progress"""
    __tablename__ = 'game_progress'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    level = Column(Integer, default=1)
    score = Column(Integer, default=0)
    experience_points = Column(Integer, default=0)
    completed_cases = Column(Integer, default=0)
    current_specialization = Column(String(100))
    unlocked_specializations = Column(Text)  # JSON serialized list of unlocked specializations
    unlocked_treatments = Column(Text)  # JSON serialized list of unlocked treatments
    unlocked_tests = Column(Text)  # JSON serialized list of unlocked tests
    achievements = Column(Text)  # JSON serialized list of achievements
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="game_progress")
    doctor = relationship("Doctor")
    
    def to_dict(self):
        """Convert to dictionary representation"""
        specializations_str = str(self.unlocked_specializations) if self.unlocked_specializations is not None else None
        treatments_str = str(self.unlocked_treatments) if self.unlocked_treatments is not None else None
        tests_str = str(self.unlocked_tests) if self.unlocked_tests is not None else None
        achievements_str = str(self.achievements) if self.achievements is not None else None
        
        return {
            'id': self.id,
            'user_id': self.user_id,
            'doctor_id': self.doctor_id,
            'level': self.level,
            'score': self.score,
            'experience_points': self.experience_points,
            'completed_cases': self.completed_cases,
            'current_specialization': self.current_specialization,
            'unlocked_specializations': json.loads(specializations_str) if specializations_str else [],
            'unlocked_treatments': json.loads(treatments_str) if treatments_str else [],
            'unlocked_tests': json.loads(tests_str) if tests_str else [],
            'achievements': json.loads(achievements_str) if achievements_str else [],
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }


# Association table for many-to-many relationship between users and doctors
user_doctors = Table('user_doctors', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('doctor_id', Integer, ForeignKey('doctors.id'), primary_key=True)
)

class Medication(Base):
    """Database model for medications"""
    __tablename__ = 'medications'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    dosages = Column(Text)  # JSON serialized list
    administration_routes = Column(Text)  # JSON serialized list
    indications = Column(Text)  # JSON serialized list
    contraindications = Column(Text)  # JSON serialized list
    side_effects = Column(Text)  # JSON serialized complex structure
    interactions = Column(Text)  # JSON serialized list
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    medication_records = relationship("MedicationRecord", back_populates="medication", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert to dictionary representation"""
        dosages_str = str(self.dosages) if self.dosages is not None else None
        routes_str = str(self.administration_routes) if self.administration_routes is not None else None
        indications_str = str(self.indications) if self.indications is not None else None
        contraindications_str = str(self.contraindications) if self.contraindications is not None else None
        side_effects_str = str(self.side_effects) if self.side_effects is not None else None
        interactions_str = str(self.interactions) if self.interactions is not None else None
        
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'dosages': json.loads(dosages_str) if dosages_str else [],
            'administration_routes': json.loads(routes_str) if routes_str else [],
            'indications': json.loads(indications_str) if indications_str else [],
            'contraindications': json.loads(contraindications_str) if contraindications_str else [],
            'side_effects': json.loads(side_effects_str) if side_effects_str else [],
            'interactions': json.loads(interactions_str) if interactions_str else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class MedicationRecord(Base):
    """Database model for patient medication administration records"""
    __tablename__ = 'medication_records'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(String(50), ForeignKey('patients.patient_id'), nullable=False)
    medication_id = Column(Integer, ForeignKey('medications.id'), nullable=False)
    dosage = Column(String(50), nullable=False)
    administration_route = Column(String(50), nullable=False)
    administration_time = Column(DateTime, default=datetime.now)
    effectiveness = Column(Float, nullable=True)  # Score between 0.0 and 1.0
    side_effects_experienced = Column(Text)  # JSON serialized list of side effects
    vital_changes = Column(Text)  # JSON serialized changes to vital signs
    notes = Column(Text)  # Additional notes about the medication response
    
    # Relationships
    patient = relationship("Patient", back_populates="medication_records")
    medication = relationship("Medication", back_populates="medication_records")
    
    def to_dict(self):
        """Convert to dictionary representation"""
        side_effects_str = str(self.side_effects_experienced) if self.side_effects_experienced is not None else None
        vital_changes_str = str(self.vital_changes) if self.vital_changes is not None else None
        
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'medication_id': self.medication_id,
            'medication_name': self.medication.name if self.medication else "Unknown",
            'dosage': self.dosage,
            'administration_route': self.administration_route,
            'administration_time': self.administration_time.isoformat() if self.administration_time else None,
            'effectiveness': self.effectiveness,
            'side_effects_experienced': json.loads(side_effects_str) if side_effects_str else [],
            'vital_changes': json.loads(vital_changes_str) if vital_changes_str else {},
            'notes': self.notes
        }