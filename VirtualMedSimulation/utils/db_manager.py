"""
Database manager for PostgreSQL integration
Uses SQLAlchemy to interact with the PostgreSQL database
"""

import os
import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool
from models.database_models import Base, Patient, TestResult, ImagingResult, TreatmentRecord, Doctor, MedicalCondition, User, GameProgress, Medication, MedicationRecord
from models.patient import Patient as PatientModel, VitalSigns
from models.doctor import Doctor as DoctorModel
from models.diagnosis import diagnosis_catalog
from models.medication import Medication as MedicationModel, MedicationResponse, MedicationCatalog

# Get database URL from environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create database engine with correct SSL settings for Neon PostgreSQL
if DATABASE_URL and 'neon.tech' in DATABASE_URL:
    # Keep the sslmode=require for Neon DB
    engine = create_engine(DATABASE_URL, poolclass=NullPool, echo=False)
else:
    # Fallback for other database connections
    engine = create_engine(DATABASE_URL or 'sqlite:///data/medical_data.db', poolclass=NullPool, echo=False)

# Create session factory
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def init_db():
    """Initialize the database with tables"""
    Base.metadata.create_all(engine)
    print("Database initialized with all tables")

class DBManager:
    """Manager for database operations"""
    
    @staticmethod
    def save_patient(patient_model):
        """
        Save a patient model to the database
        
        Args:
            patient_model: Patient domain model
            
        Returns:
            True if successful, False otherwise
        """
        try:
            session = Session()
            
            # Check if patient already exists
            db_patient = session.query(Patient).filter_by(patient_id=patient_model.patient_id).first()
            
            if db_patient:
                # Update existing patient
                vital_signs_dict = {}
                if patient_model.vital_signs:
                    vital_signs_dict = {
                        'pulse': patient_model.vital_signs.pulse,
                        'systolic_bp': patient_model.vital_signs.systolic_bp,
                        'diastolic_bp': patient_model.vital_signs.diastolic_bp,
                        'temperature': patient_model.vital_signs.temperature,
                        'respiratory_rate': patient_model.vital_signs.respiratory_rate,
                        'oxygen_saturation': patient_model.vital_signs.oxygen_saturation
                    }
                
                db_patient.name = patient_model.name
                db_patient.age = patient_model.age
                db_patient.gender = patient_model.gender
                db_patient.medical_history = str(patient_model.medical_history)
                db_patient.current_symptoms = str(patient_model.current_symptoms)
                db_patient.vital_signs = str(vital_signs_dict)
                db_patient.diagnosis = patient_model.diagnosis
                db_patient.condition_severity = patient_model.condition_severity
            else:
                # Create new patient
                db_patient = Patient.from_model(patient_model)
                session.add(db_patient)
            
            session.commit()
            return True
        except Exception as e:
            print(f"Error saving patient to database: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    @staticmethod
    def get_patient(patient_id):
        """
        Get a patient from the database
        
        Args:
            patient_id: Unique identifier for the patient
            
        Returns:
            Patient domain model if found, None otherwise
        """
        try:
            session = Session()
            db_patient = session.query(Patient).filter_by(patient_id=patient_id).first()
            
            if not db_patient:
                return None
            
            # Convert DB model to domain model
            import json
            
            # Parse vital signs
            vital_signs_dict = json.loads(db_patient.vital_signs) if db_patient.vital_signs else {}
            vital_signs = VitalSigns(
                pulse=vital_signs_dict.get('pulse', 80),
                systolic_bp=vital_signs_dict.get('systolic_bp', 120),
                diastolic_bp=vital_signs_dict.get('diastolic_bp', 80),
                temperature=vital_signs_dict.get('temperature', 36.6),
                respiratory_rate=vital_signs_dict.get('respiratory_rate', 16),
                oxygen_saturation=vital_signs_dict.get('oxygen_saturation', 98)
            )
            
            # Parse medical history and symptoms
            medical_history = json.loads(db_patient.medical_history) if db_patient.medical_history else []
            current_symptoms = json.loads(db_patient.current_symptoms) if db_patient.current_symptoms else []
            
            # Create domain model
            patient_model = PatientModel(
                patient_id=db_patient.patient_id,
                name=db_patient.name,
                age=db_patient.age,
                gender=db_patient.gender,
                medical_history=medical_history,
                current_symptoms=current_symptoms,
                vital_signs=vital_signs,
                diagnosis=db_patient.diagnosis,
                condition_severity=db_patient.condition_severity
            )
            
            # Load treatments and tests
            treatment_records = session.query(TreatmentRecord).filter_by(patient_id=patient_id).all()
            test_results = session.query(TestResult).filter_by(patient_id=patient_id).all()
            
            for treatment in treatment_records:
                treatment_dict = {
                    'treatment': treatment.treatment_name,
                    'time': treatment.treatment_time.strftime("%Y-%m-%d %H:%M:%S")
                }
                patient_model.treatments_applied.append(treatment_dict)
            
            for test in test_results:
                test_dict = {
                    'test': test.test_name,
                    'time': test.test_time.strftime("%Y-%m-%d %H:%M:%S")
                }
                patient_model.tests_performed.append(test_dict)
            
            return patient_model
        except Exception as e:
            print(f"Error getting patient from database: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def get_all_patients():
        """
        Get all patients from the database
        
        Returns:
            List of Patient domain models
        """
        try:
            session = Session()
            db_patients = session.query(Patient).all()
            
            patients = []
            for db_patient in db_patients:
                patient = DBManager.get_patient(db_patient.patient_id)
                if patient:
                    patients.append(patient)
            
            return patients
        except Exception as e:
            print(f"Error getting all patients from database: {e}")
            return []
        finally:
            session.close()
    
    @staticmethod
    def save_test_result(patient_id, test_name, result):
        """
        Save a test result to the database
        
        Args:
            patient_id: Patient ID
            test_name: Name of the test
            result: Test result data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            session = Session()
            
            # Check if patient exists
            db_patient = session.query(Patient).filter_by(patient_id=patient_id).first()
            if not db_patient:
                print(f"Patient {patient_id} not found in database")
                return False
            
            # Create test result
            import json
            test_result = TestResult(
                patient_id=patient_id,
                test_name=test_name,
                results=json.dumps(result),
                is_abnormal=result.get('is_abnormal', False)
            )
            
            # Check for image path and save as imaging result if present
            if 'details' in result and 'image_path' in result['details']:
                image_path = result['details']['image_path']
                image_type = test_name
                description = result.get('interpretation', '')
                
                imaging_result = ImagingResult(
                    patient_id=patient_id,
                    image_type=image_type,
                    image_path=image_path,
                    description=description
                )
                
                session.add(imaging_result)
            
            session.add(test_result)
            session.commit()
            return True
        except Exception as e:
            print(f"Error saving test result to database: {e}")
            session.rollback()
            return False
        finally:
            session.close()
            
    @staticmethod
    def save_imaging_result(patient_id, image_type, image_path, description=""):
        """
        Save an imaging result to the database
        
        Args:
            patient_id: Patient ID
            image_type: Type of image (X-ray, ECG, etc)
            image_path: Path to the image file
            description: Description of the image findings
            
        Returns:
            True if successful, False otherwise
        """
        try:
            session = Session()
            
            # Check if patient exists
            db_patient = session.query(Patient).filter_by(patient_id=patient_id).first()
            if not db_patient:
                print(f"Patient {patient_id} not found in database")
                return False
            
            # Create imaging result
            imaging_result = ImagingResult(
                patient_id=patient_id,
                image_type=image_type,
                image_path=image_path,
                description=description
            )
            
            session.add(imaging_result)
            session.commit()
            print(f"Saved {image_type} image for patient {patient_id}")
            return True
        except Exception as e:
            print(f"Error saving imaging result to database: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    @staticmethod
    def save_treatment_record(patient_id, treatment_name, result):
        """
        Save a treatment record to the database
        
        Args:
            patient_id: Patient ID
            treatment_name: Name of the treatment
            result: Treatment result data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            session = Session()
            
            # Check if patient exists
            db_patient = session.query(Patient).filter_by(patient_id=patient_id).first()
            if not db_patient:
                print(f"Patient {patient_id} not found in database")
                return False
            
            # Create treatment record
            import json
            treatment_record = TreatmentRecord(
                patient_id=patient_id,
                treatment_name=treatment_name,
                effects=json.dumps(result.get('effects', [])),
                vital_changes=json.dumps(result.get('vital_changes', {}))
            )
            
            session.add(treatment_record)
            session.commit()
            return True
        except Exception as e:
            print(f"Error saving treatment record to database: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    @staticmethod
    def save_doctor(doctor_model):
        """
        Save a doctor model to the database
        
        Args:
            doctor_model: Doctor domain model
            
        Returns:
            True if successful, False otherwise
        """
        try:
            session = Session()
            
            # Check if doctor exists by name
            db_doctor = session.query(Doctor).filter_by(name=doctor_model.name).first()
            
            if db_doctor:
                # Update existing doctor
                db_doctor.specialization = doctor_model.specialization.name if doctor_model.specialization else ""
                db_doctor.experience = doctor_model.experience
                db_doctor.patients_treated = doctor_model.patients_treated
                db_doctor.successful_diagnoses = doctor_model.successful_diagnoses
                db_doctor.score = doctor_model.score
            else:
                # Create new doctor
                db_doctor = Doctor(
                    name=doctor_model.name,
                    specialization=doctor_model.specialization.name if doctor_model.specialization else "",
                    experience=doctor_model.experience,
                    patients_treated=doctor_model.patients_treated,
                    successful_diagnoses=doctor_model.successful_diagnoses,
                    score=doctor_model.score
                )
                session.add(db_doctor)
            
            session.commit()
            return True
        except Exception as e:
            print(f"Error saving doctor to database: {e}")
            session.rollback()
            return False
        finally:
            session.close()
    
    @staticmethod
    def get_doctor(name):
        """
        Get a doctor from the database
        
        Args:
            name: Doctor's name
            
        Returns:
            Doctor domain model if found, None otherwise
        """
        try:
            session = Session()
            db_doctor = session.query(Doctor).filter_by(name=name).first()
            
            if not db_doctor:
                return None
            
            # Create domain model
            from models.doctor import Specialization
            
            # Get specialization
            specialization = None
            for spec in get_specializations():
                if spec.name == db_doctor.specialization:
                    specialization = spec
                    break
            
            doctor_model = DoctorModel(
                name=db_doctor.name,
                specialization=specialization,
                experience=db_doctor.experience
            )
            
            # Set statistics
            doctor_model.patients_treated = db_doctor.patients_treated
            doctor_model.successful_diagnoses = db_doctor.successful_diagnoses
            doctor_model.score = db_doctor.score
            
            return doctor_model
        except Exception as e:
            print(f"Error getting doctor from database: {e}")
            return None
        finally:
            session.close()
    
    @staticmethod
    def initialize_conditions():
        """
        Initialize medical conditions in the database from diagnosis catalog
        
        Returns:
            Number of conditions added
        """
        try:
            session = Session()
            count = 0
            
            # Get all diagnoses from catalog
            for diagnosis in diagnosis_catalog.get_all_diagnoses():
                # Check if condition already exists
                db_condition = session.query(MedicalCondition).filter_by(name=diagnosis.name).first()
                
                import json
                
                if db_condition:
                    # Update existing condition
                    db_condition.description = diagnosis.description
                    db_condition.symptoms = json.dumps(diagnosis.primary_symptoms + diagnosis.secondary_symptoms)
                    db_condition.recommended_tests = json.dumps(diagnosis.recommended_tests)
                    db_condition.recommended_treatments = json.dumps(diagnosis.recommended_treatments)
                    db_condition.severity = diagnosis.severity
                else:
                    # Create new condition
                    db_condition = MedicalCondition(
                        name=diagnosis.name,
                        description=diagnosis.description,
                        symptoms=json.dumps(diagnosis.primary_symptoms + diagnosis.secondary_symptoms),
                        recommended_tests=json.dumps(diagnosis.recommended_tests),
                        recommended_treatments=json.dumps(diagnosis.recommended_treatments),
                        severity=diagnosis.severity
                    )
                    session.add(db_condition)
                    count += 1
            
            session.commit()
            return count
        except Exception as e:
            print(f"Error initializing medical conditions in database: {e}")
            session.rollback()
            return 0
        finally:
            session.close()


    @staticmethod
    def register_user(username, email, password):
        """
        Register a new user
        
        Args:
            username: Username
            email: Email address
            password: Plain text password
            
        Returns:
            User object if registration successful, None otherwise
        """
        try:
            session = Session()
            
            # Check if user already exists
            existing_user = session.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                print(f"User with username '{username}' or email '{email}' already exists")
                return None
                
            # Create new user
            new_user = User(
                username=username,
                email=email
            )
            new_user.set_password(password)
            
            session.add(new_user)
            session.commit()
            
            print(f"User {username} registered successfully")
            return new_user.to_dict()
        except Exception as e:
            print(f"Error registering user: {e}")
            if 'session' in locals():
                session.rollback()
            return None
        finally:
            if 'session' in locals():
                session.close()
                
    @staticmethod
    def authenticate_user(username_or_email, password):
        """
        Authenticate a user
        
        Args:
            username_or_email: Username or email
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        try:
            session = Session()
            
            # Find user by username or email
            user = session.query(User).filter(
                (User.username == username_or_email) | (User.email == username_or_email)
            ).first()
            
            if not user:
                print(f"User not found: {username_or_email}")
                return None
                
            # Check password
            if not user.check_password(str(password)):
                print("Invalid password")
                return None
                
            # Update last login time
            user.last_login = datetime.now()
            session.commit()
            
            print(f"User {user.username} authenticated successfully")
            return user.to_dict()
        except Exception as e:
            print(f"Error authenticating user: {e}")
            if 'session' in locals():
                session.rollback()
            return None
        finally:
            if 'session' in locals():
                session.close()
    
    @staticmethod
    def update_last_login(user_id):
        """
        Update the last login timestamp for a user
        
        Args:
            user_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            session = Session()
            
            # Find user by ID
            user = session.query(User).filter_by(id=user_id).first()
            
            if not user:
                return False
            
            # Update last login time
            user.last_login = datetime.now()
            session.commit()
            
            return True
        except Exception as e:
            print(f"Error updating last login: {e}")
            if 'session' in locals():
                session.rollback()
            return False
        finally:
            if 'session' in locals():
                session.close()
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User dict if found, None otherwise
        """
        try:
            session = Session()
            
            # Find user by ID
            user = session.query(User).filter_by(id=user_id).first()
            
            if not user:
                return None
                
            return user.to_dict()
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None
        finally:
            if 'session' in locals():
                session.close()
    
    @staticmethod
    def get_user_progress(user_id):
        """
        Get user game progress
        
        Args:
            user_id: User ID
            
        Returns:
            List of game progress objects
        """
        try:
            session = Session()
            
            progress_records = session.query(GameProgress).filter_by(user_id=user_id).all()
            
            return [progress.to_dict() for progress in progress_records]
        except Exception as e:
            print(f"Error getting user progress: {e}")
            return []
        finally:
            if 'session' in locals():
                session.close()
                
    @staticmethod
    def save_game_progress(user_id, doctor_id, progress_data):
        """
        Save game progress
        
        Args:
            user_id: User ID
            doctor_id: Doctor ID
            progress_data: Dictionary containing progress data
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            session = Session()
            
            # Check if user has existing progress with this doctor
            existing_progress = session.query(GameProgress).filter_by(
                user_id=user_id, 
                doctor_id=doctor_id
            ).first()
            
            if existing_progress:
                # Update existing progress
                if 'level' in progress_data:
                    existing_progress.level = progress_data['level']
                if 'score' in progress_data:
                    existing_progress.score = progress_data['score']
                if 'experience_points' in progress_data:
                    existing_progress.experience_points = progress_data['experience_points']
                if 'completed_cases' in progress_data:
                    existing_progress.completed_cases = progress_data['completed_cases']
                if 'current_specialization' in progress_data:
                    existing_progress.current_specialization = progress_data['current_specialization']
                
                # Handle JSON fields
                if 'unlocked_specializations' in progress_data:
                    existing_progress.unlocked_specializations = json.dumps(progress_data['unlocked_specializations'])
                if 'unlocked_treatments' in progress_data:
                    existing_progress.unlocked_treatments = json.dumps(progress_data['unlocked_treatments'])
                if 'unlocked_tests' in progress_data:
                    existing_progress.unlocked_tests = json.dumps(progress_data['unlocked_tests'])
                if 'achievements' in progress_data:
                    existing_progress.achievements = json.dumps(progress_data['achievements'])
            else:
                # Create new progress record
                new_progress = GameProgress(
                    user_id=user_id,
                    doctor_id=doctor_id,
                    level=progress_data.get('level', 1),
                    score=progress_data.get('score', 0),
                    experience_points=progress_data.get('experience_points', 0),
                    completed_cases=progress_data.get('completed_cases', 0),
                    current_specialization=progress_data.get('current_specialization', ''),
                    unlocked_specializations=json.dumps(progress_data.get('unlocked_specializations', [])),
                    unlocked_treatments=json.dumps(progress_data.get('unlocked_treatments', [])),
                    unlocked_tests=json.dumps(progress_data.get('unlocked_tests', [])),
                    achievements=json.dumps(progress_data.get('achievements', []))
                )
                session.add(new_progress)
                
            session.commit()
            print(f"Game progress saved for user {user_id}")
            return True
        except Exception as e:
            print(f"Error saving game progress: {e}")
            if 'session' in locals():
                session.rollback()
            return False
        finally:
            if 'session' in locals():
                session.close()


def get_specializations():
    """Helper function to get specializations for doctor creation"""
    from models.doctor import get_available_specializations
    return get_available_specializations()


# Medication management methods
    @classmethod
    def initialize_medications(cls):
        """Initialize the database with medications from the catalog"""
        try:
            session = Session()
            
            # Check if medications already exist in the database
            if session.query(Medication).count() > 0:
                print("Medications already exist in database, skipping initialization")
                return
            
            # Get the medication catalog
            catalog = MedicationCatalog()
            
            # Add all medications to the database
            for med in catalog.get_all_medications():
                db_med = Medication(
                    name=med.name,
                    category=med.category,
                    description=med.description,
                    dosages=json.dumps(med.dosages),
                    administration_routes=json.dumps(med.administration_routes),
                    indications=json.dumps(med.indications),
                    contraindications=json.dumps(med.contraindications),
                    side_effects=json.dumps(med.side_effects),
                    interactions=json.dumps(med.interactions)
                )
                session.add(db_med)
            
            session.commit()
            print(f"Added {len(catalog.get_all_medications())} medications to database")
            
        except Exception as e:
            print(f"Error initializing medications: {e}")
            if 'session' in locals():
                session.rollback()
        finally:
            if 'session' in locals():
                session.close()
                
    @classmethod
    def get_all_medications(cls):
        """Get all medications from the database"""
        try:
            session = Session()
            medications = session.query(Medication).all()
            return [med.to_dict() for med in medications]
        except Exception as e:
            print(f"Error getting medications: {e}")
            return []
        finally:
            if 'session' in locals():
                session.close()
    
    @classmethod
    def get_medication_by_name(cls, name):
        """Get a medication by name"""
        try:
            session = Session()
            medication = session.query(Medication).filter(Medication.name == name).first()
            return medication.to_dict() if medication else None
        except Exception as e:
            print(f"Error getting medication: {e}")
            return None
        finally:
            if 'session' in locals():
                session.close()
    
    @classmethod
    def get_medications_by_category(cls, category):
        """Get all medications in a specific category"""
        try:
            session = Session()
            medications = session.query(Medication).filter(Medication.category == category).all()
            return [med.to_dict() for med in medications]
        except Exception as e:
            print(f"Error getting medications by category: {e}")
            return []
        finally:
            if 'session' in locals():
                session.close()
    
    @classmethod
    def administer_medication(cls, patient_id, medication_name, dosage, route):
        """
        Administer a medication to a patient and record the response
        
        Args:
            patient_id: The patient's unique ID
            medication_name: Name of the medication to administer
            dosage: Dosage to administer
            route: Administration route
            
        Returns:
            Dictionary with administration results
        """
        try:
            session = Session()
            
            # Get the patient
            patient_db = session.query(Patient).filter(Patient.patient_id == patient_id).first()
            if not patient_db:
                print(f"Patient {patient_id} not found")
                return {"success": False, "error": "Patient not found"}
            
            # Get the medication
            medication_db = session.query(Medication).filter(Medication.name == medication_name).first()
            if not medication_db:
                print(f"Medication {medication_name} not found")
                return {"success": False, "error": "Medication not found"}
            
            # Create domain models for simulation
            patient_model = cls._create_patient_model(patient_db)
            
            medication_model = MedicationModel(
                name=medication_db.name,
                category=medication_db.category,
                description=medication_db.description,
                dosages=json.loads(medication_db.dosages) if medication_db.dosages else [],
                administration_routes=json.loads(medication_db.administration_routes) if medication_db.administration_routes else [],
                indications=json.loads(medication_db.indications) if medication_db.indications else [],
                contraindications=json.loads(medication_db.contraindications) if medication_db.contraindications else [],
                side_effects=json.loads(medication_db.side_effects) if medication_db.side_effects else [],
                interactions=json.loads(medication_db.interactions) if medication_db.interactions else []
            )
            
            # Simulate the patient's response
            medication_response = MedicationResponse(patient_model, medication_model, dosage, route)
            response = medication_response.simulate_response()
            
            # Save the medication record
            medication_record = MedicationRecord(
                patient_id=patient_id,
                medication_id=medication_db.id,
                dosage=dosage,
                administration_route=route,
                effectiveness=response.get('effectiveness', 0.0),
                side_effects_experienced=json.dumps(response.get('side_effects', [])),
                vital_changes=json.dumps(response.get('vital_changes', {})),
                notes=response.get('response_text', '')
            )
            session.add(medication_record)
            
            # Update patient's vital signs based on the medication response
            vital_changes = response.get('vital_changes', {})
            if vital_changes:
                current_vitals = json.loads(patient_db.vital_signs) if patient_db.vital_signs else {}
                
                if 'pulse' in vital_changes and 'pulse' in current_vitals:
                    current_vitals['pulse'] += vital_changes['pulse']
                
                if 'systolic_bp' in vital_changes and 'systolic_bp' in current_vitals:
                    current_vitals['systolic_bp'] += vital_changes['systolic_bp']
                
                if 'diastolic_bp' in vital_changes and 'diastolic_bp' in current_vitals:
                    current_vitals['diastolic_bp'] += vital_changes['diastolic_bp']
                
                if 'temperature' in vital_changes and 'temperature' in current_vitals:
                    current_vitals['temperature'] += vital_changes['temperature']
                
                if 'respiratory_rate' in vital_changes and 'respiratory_rate' in current_vitals:
                    current_vitals['respiratory_rate'] += vital_changes['respiratory_rate']
                
                if 'oxygen_saturation' in vital_changes and 'oxygen_saturation' in current_vitals:
                    current_vitals['oxygen_saturation'] += vital_changes['oxygen_saturation']
                
                # Update the patient's vital signs
                patient_db.vital_signs = json.dumps(current_vitals)
            
            session.commit()
            
            # Return the administration results
            return {
                "success": True,
                "medication": medication_db.name,
                "dosage": dosage,
                "route": route,
                "effectiveness": response.get('effectiveness', 0.0),
                "side_effects": response.get('side_effects', []),
                "vital_changes": response.get('vital_changes', {}),
                "response_text": response.get('response_text', '')
            }
            
        except Exception as e:
            print(f"Error administering medication: {e}")
            if 'session' in locals():
                session.rollback()
            return {"success": False, "error": str(e)}
        finally:
            if 'session' in locals():
                session.close()
    
    @classmethod
    def get_patient_medication_history(cls, patient_id):
        """Get the medication history for a patient"""
        try:
            session = Session()
            
            # Get all medication records for the patient
            records = session.query(MedicationRecord).join(Medication).filter(
                MedicationRecord.patient_id == patient_id
            ).order_by(MedicationRecord.administration_time.desc()).all()
            
            return [record.to_dict() for record in records]
            
        except Exception as e:
            print(f"Error getting medication history: {e}")
            return []
        finally:
            if 'session' in locals():
                session.close()
    
    @classmethod
    def _create_patient_model(cls, patient_db):
        """Create a domain model from a database patient model"""
        # Convert JSON strings to Python objects
        medical_history = json.loads(patient_db.medical_history) if patient_db.medical_history else []
        current_symptoms = json.loads(patient_db.current_symptoms) if patient_db.current_symptoms else []
        vital_signs_dict = json.loads(patient_db.vital_signs) if patient_db.vital_signs else {}
        
        # Create vital signs object
        vital_signs = VitalSigns(
            pulse=vital_signs_dict.get('pulse', 0),
            systolic_bp=vital_signs_dict.get('systolic_bp', 0),
            diastolic_bp=vital_signs_dict.get('diastolic_bp', 0),
            temperature=vital_signs_dict.get('temperature', 0),
            respiratory_rate=vital_signs_dict.get('respiratory_rate', 0),
            oxygen_saturation=vital_signs_dict.get('oxygen_saturation', 0)
        )
        
        # Create patient model
        patient_model = PatientModel(
            patient_id=patient_db.patient_id,
            name=patient_db.name,
            age=patient_db.age,
            gender=patient_db.gender,
            medical_history=medical_history,
            current_symptoms=current_symptoms,
            vital_signs=vital_signs,
            diagnosis=patient_db.diagnosis
        )
        
        return patient_model


# Initialize the database when this module is imported
init_db()