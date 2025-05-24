import os
import sqlite3
from typing import List, Dict, Any, Optional
import json
import random

from models.patient import Patient, VitalSigns
from models.doctor import Specialization

class Database:
    """
    Database manager for VirtualDoctor simulation game.
    Uses SQLite to store and retrieve medical data.
    """
    
    def __init__(self, db_path: str = "data/medical_data.db"):
        """
        Initialize the database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Set up database
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.cursor = self.connection.cursor()
        
        # Initialize tables if they don't exist
        self._initialize_tables()
    
    def _initialize_tables(self) -> None:
        """Create database tables if they don't exist."""
        # Patients table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            medical_history TEXT,  -- JSON list
            current_symptoms TEXT,  -- JSON list
            vital_signs TEXT,  -- JSON object
            diagnosis TEXT DEFAULT NULL,
            condition_severity INTEGER DEFAULT 1,
            admission_time TEXT,
            treatments_applied TEXT DEFAULT "[]",  -- JSON list of objects
            tests_performed TEXT DEFAULT "[]"  -- JSON list of objects
        )
        ''')
        
        # Test results table for storing detailed test results
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            test_name TEXT NOT NULL,
            test_time TEXT NOT NULL,
            results TEXT NOT NULL,  -- JSON object
            FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
        )
        ''')
        
        # Imaging results table for storing medical images (X-rays, ECGs, etc.)
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS imaging_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            image_type TEXT NOT NULL,  -- X-ray, ECG, etc.
            image_path TEXT NOT NULL,  -- Path to image file
            description TEXT,
            test_time TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
        )
        ''')
        
        # Medical conditions/diseases reference table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS medical_conditions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            symptoms TEXT NOT NULL,  -- JSON list
            recommended_tests TEXT NOT NULL,  -- JSON list
            recommended_treatments TEXT NOT NULL,  -- JSON list
            severity INTEGER NOT NULL
        )
        ''')
        
        # Diagnostic tests reference table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnostic_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            required_equipment TEXT,  -- JSON list
            specialization TEXT,  -- Specialization that can perform this test
            accuracy REAL,  -- Accuracy percentage
            invasiveness INTEGER  -- Scale 1-10
        )
        ''')
        
        # Medications/treatments reference table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            effects TEXT NOT NULL,  -- JSON object
            side_effects TEXT,  -- JSON list
            specialization TEXT,  -- Specialization that can administer this
            dosage TEXT
        )
        ''')
        
        # Commit the changes
        self.connection.commit()
    
    def close(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
    
    def save_patient(self, patient: Patient) -> bool:
        """
        Save a patient to the database, updating if patient_id exists.
        
        Args:
            patient: Patient object to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert VitalSigns to dictionary
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
            
            # Check if patient already exists
            self.cursor.execute(
                "SELECT id FROM patients WHERE patient_id = ?", 
                (patient.patient_id,)
            )
            result = self.cursor.fetchone()
            
            if result:
                # Update existing patient
                self.cursor.execute('''
                UPDATE patients SET
                    name = ?,
                    age = ?,
                    gender = ?,
                    medical_history = ?,
                    current_symptoms = ?,
                    vital_signs = ?,
                    diagnosis = ?,
                    condition_severity = ?,
                    treatments_applied = ?,
                    tests_performed = ?
                WHERE patient_id = ?
                ''', (
                    patient.name,
                    patient.age,
                    patient.gender,
                    json.dumps(patient.medical_history),
                    json.dumps(patient.current_symptoms),
                    json.dumps(vital_signs_dict),
                    patient.diagnosis,
                    patient.condition_severity,
                    json.dumps(patient.treatments_applied),
                    json.dumps(patient.tests_performed),
                    patient.patient_id
                ))
            else:
                # Insert new patient
                self.cursor.execute('''
                INSERT INTO patients (
                    patient_id, name, age, gender, medical_history, current_symptoms, 
                    vital_signs, diagnosis, condition_severity, admission_time,
                    treatments_applied, tests_performed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    patient.patient_id,
                    patient.name,
                    patient.age,
                    patient.gender,
                    json.dumps(patient.medical_history),
                    json.dumps(patient.current_symptoms),
                    json.dumps(vital_signs_dict),
                    patient.diagnosis,
                    patient.condition_severity,
                    patient.admission_time.strftime("%Y-%m-%d %H:%M:%S"),
                    json.dumps(patient.treatments_applied),
                    json.dumps(patient.tests_performed)
                ))
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving patient: {e}")
            return False
    
    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """
        Get a patient from the database.
        
        Args:
            patient_id: Unique identifier for the patient
            
        Returns:
            Patient object if found, None otherwise
        """
        try:
            self.cursor.execute(
                "SELECT * FROM patients WHERE patient_id = ?", 
                (patient_id,)
            )
            data = self.cursor.fetchone()
            
            if not data:
                return None
            
            # Convert to dictionary
            patient_dict = dict(data)
            
            # Convert JSON strings back to objects
            patient_dict['medical_history'] = json.loads(patient_dict['medical_history'])
            patient_dict['current_symptoms'] = json.loads(patient_dict['current_symptoms'])
            
            # Create VitalSigns
            vital_signs_dict = json.loads(patient_dict['vital_signs'])
            vital_signs = VitalSigns(
                pulse=vital_signs_dict.get('pulse', 80),
                systolic_bp=vital_signs_dict.get('systolic_bp', 120),
                diastolic_bp=vital_signs_dict.get('diastolic_bp', 80),
                temperature=vital_signs_dict.get('temperature', 36.6),
                respiratory_rate=vital_signs_dict.get('respiratory_rate', 16),
                oxygen_saturation=vital_signs_dict.get('oxygen_saturation', 98)
            )
            
            # Load treatments and tests
            treatments = json.loads(patient_dict['treatments_applied'])
            tests = json.loads(patient_dict['tests_performed'])
            
            # Create and return patient
            patient = Patient(
                patient_id=patient_dict['patient_id'],
                name=patient_dict['name'],
                age=patient_dict['age'],
                gender=patient_dict['gender'],
                medical_history=patient_dict['medical_history'],
                current_symptoms=patient_dict['current_symptoms'],
                vital_signs=vital_signs,
                diagnosis=patient_dict['diagnosis'],
                condition_severity=patient_dict['condition_severity']
            )
            
            # Set treatments and tests
            patient.treatments_applied = treatments
            patient.tests_performed = tests
            
            return patient
        except Exception as e:
            print(f"Error getting patient: {e}")
            return None
    
    def get_all_patients(self) -> List[Patient]:
        """
        Get all patients from the database.
        
        Returns:
            List of Patient objects
        """
        patients = []
        try:
            self.cursor.execute("SELECT patient_id FROM patients")
            patient_ids = [row['patient_id'] for row in self.cursor.fetchall()]
            
            for patient_id in patient_ids:
                patient = self.get_patient(patient_id)
                if patient:
                    patients.append(patient)
            
            return patients
        except Exception as e:
            print(f"Error getting all patients: {e}")
            return []
    
    def delete_patient(self, patient_id: str) -> bool:
        """
        Delete a patient from the database.
        
        Args:
            patient_id: Unique identifier for the patient
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.cursor.execute(
                "DELETE FROM patients WHERE patient_id = ?", 
                (patient_id,)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting patient: {e}")
            return False
    
    def save_test_result(self, patient_id: str, test_name: str, results: Dict) -> bool:
        """
        Save a test result to the database.
        
        Args:
            patient_id: Patient ID the test was performed on
            test_name: Name of the test performed
            results: Dictionary with test results
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from datetime import datetime
            
            # Insert test result
            self.cursor.execute('''
            INSERT INTO test_results (
                patient_id, test_name, test_time, results
            ) VALUES (?, ?, ?, ?)
            ''', (
                patient_id,
                test_name,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                json.dumps(results)
            ))
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving test result: {e}")
            return False
    
    def get_test_results(self, patient_id: str, test_name: Optional[str] = None) -> List[Dict]:
        """
        Get test results for a patient.
        
        Args:
            patient_id: Patient ID to get results for
            test_name: Optional test name to filter by
            
        Returns:
            List of test result dictionaries
        """
        try:
            if test_name:
                self.cursor.execute(
                    "SELECT * FROM test_results WHERE patient_id = ? AND test_name = ? ORDER BY test_time DESC", 
                    (patient_id, test_name)
                )
            else:
                self.cursor.execute(
                    "SELECT * FROM test_results WHERE patient_id = ? ORDER BY test_time DESC", 
                    (patient_id,)
                )
            
            results = []
            for row in self.cursor.fetchall():
                result_dict = dict(row)
                result_dict['results'] = json.loads(result_dict['results'])
                results.append(result_dict)
            
            return results
        except Exception as e:
            print(f"Error getting test results: {e}")
            return []
    
    def save_imaging_result(self, patient_id: str, image_type: str, image_path: str, description: str) -> bool:
        """
        Save an imaging result to the database.
        
        Args:
            patient_id: Patient ID the image is for
            image_type: Type of image (X-ray, ECG, etc.)
            image_path: Path to the stored image file
            description: Description of the image findings
            
        Returns:
            True if successful, False otherwise
        """
        try:
            from datetime import datetime
            
            # Insert imaging result
            self.cursor.execute('''
            INSERT INTO imaging_results (
                patient_id, image_type, image_path, description, test_time
            ) VALUES (?, ?, ?, ?, ?)
            ''', (
                patient_id,
                image_type,
                image_path,
                description,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving imaging result: {e}")
            return False
    
    def get_imaging_results(self, patient_id: str, image_type: Optional[str] = None) -> List[Dict]:
        """
        Get imaging results for a patient.
        
        Args:
            patient_id: Patient ID to get images for
            image_type: Optional image type to filter by
            
        Returns:
            List of imaging result dictionaries
        """
        try:
            if image_type:
                self.cursor.execute(
                    "SELECT * FROM imaging_results WHERE patient_id = ? AND image_type = ? ORDER BY test_time DESC", 
                    (patient_id, image_type)
                )
            else:
                self.cursor.execute(
                    "SELECT * FROM imaging_results WHERE patient_id = ? ORDER BY test_time DESC", 
                    (patient_id,)
                )
            
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error getting imaging results: {e}")
            return []
    
    def save_medical_condition(self, name: str, description: str, symptoms: List[str], 
                           recommended_tests: List[str], recommended_treatments: List[str], 
                           severity: int) -> bool:
        """
        Save a medical condition to the database.
        
        Args:
            name: Condition name
            description: Condition description
            symptoms: List of symptoms
            recommended_tests: List of recommended tests
            recommended_treatments: List of recommended treatments
            severity: Condition severity (1-10)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if condition already exists
            self.cursor.execute("SELECT id FROM medical_conditions WHERE name = ?", (name,))
            result = self.cursor.fetchone()
            
            if result:
                # Update existing condition
                self.cursor.execute('''
                UPDATE medical_conditions SET
                    description = ?,
                    symptoms = ?,
                    recommended_tests = ?,
                    recommended_treatments = ?,
                    severity = ?
                WHERE name = ?
                ''', (
                    description,
                    json.dumps(symptoms),
                    json.dumps(recommended_tests),
                    json.dumps(recommended_treatments),
                    severity,
                    name
                ))
            else:
                # Insert new condition
                self.cursor.execute('''
                INSERT INTO medical_conditions (
                    name, description, symptoms, recommended_tests, 
                    recommended_treatments, severity
                ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    name,
                    description,
                    json.dumps(symptoms),
                    json.dumps(recommended_tests),
                    json.dumps(recommended_treatments),
                    severity
                ))
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving medical condition: {e}")
            return False
    
    def get_medical_condition(self, name: str) -> Optional[Dict]:
        """
        Get a medical condition from the database.
        
        Args:
            name: Name of the condition
            
        Returns:
            Dictionary with condition data if found, None otherwise
        """
        try:
            self.cursor.execute(
                "SELECT * FROM medical_conditions WHERE name = ?", 
                (name,)
            )
            data = self.cursor.fetchone()
            
            if not data:
                return None
            
            condition_dict = dict(data)
            
            # Convert JSON strings back to objects
            condition_dict['symptoms'] = json.loads(condition_dict['symptoms'])
            condition_dict['recommended_tests'] = json.loads(condition_dict['recommended_tests'])
            condition_dict['recommended_treatments'] = json.loads(condition_dict['recommended_treatments'])
            
            return condition_dict
        except Exception as e:
            print(f"Error getting medical condition: {e}")
            return None
    
    def get_all_medical_conditions(self) -> List[Dict]:
        """
        Get all medical conditions from the database.
        
        Returns:
            List of condition dictionaries
        """
        try:
            self.cursor.execute("SELECT name FROM medical_conditions")
            condition_names = [row['name'] for row in self.cursor.fetchall()]
            
            conditions = []
            for name in condition_names:
                condition = self.get_medical_condition(name)
                if condition:
                    conditions.append(condition)
            
            return conditions
        except Exception as e:
            print(f"Error getting all medical conditions: {e}")
            return []
    
    def initialize_sample_data(self) -> None:
        """
        Initialize the database with sample data if tables are empty.
        """
        # Check if medical conditions table is empty
        self.cursor.execute("SELECT COUNT(*) as count FROM medical_conditions")
        condition_count = self.cursor.fetchone()['count']
        
        if condition_count == 0:
            # Add sample medical conditions
            from models.diagnosis import diagnosis_catalog
            for diagnosis in diagnosis_catalog.get_all_diagnoses():
                self.save_medical_condition(
                    name=diagnosis.name,
                    description=diagnosis.description,
                    symptoms=diagnosis.primary_symptoms + diagnosis.secondary_symptoms,
                    recommended_tests=diagnosis.recommended_tests,
                    recommended_treatments=diagnosis.recommended_treatments,
                    severity=diagnosis.severity
                )
            
            print("Initialized medical conditions database")
        
        # Check if diagnostic tests table is empty
        self.cursor.execute("SELECT COUNT(*) as count FROM diagnostic_tests")
        test_count = self.cursor.fetchone()['count']
        
        if test_count == 0:
            # Add sample diagnostic tests
            tests = [
                {
                    "name": "ECG/EKG",
                    "description": "Records the electrical activity of the heart",
                    "required_equipment": ["ECG Machine", "Electrodes"],
                    "specialization": "Cardiology",
                    "accuracy": 0.95,
                    "invasiveness": 1
                },
                {
                    "name": "Chest X-Ray",
                    "description": "Imaging of the chest, lungs, heart, and blood vessels",
                    "required_equipment": ["X-Ray Machine", "Radiographic Film"],
                    "specialization": "Radiology",
                    "accuracy": 0.9,
                    "invasiveness": 2
                },
                {
                    "name": "Basic Blood Test",
                    "description": "Analysis of blood cells, chemistry, and compounds",
                    "required_equipment": ["Blood Collection Kit", "Lab Equipment"],
                    "specialization": "General Practice",
                    "accuracy": 0.98,
                    "invasiveness": 3
                },
                {
                    "name": "Blood Pressure",
                    "description": "Measurement of the pressure of circulating blood",
                    "required_equipment": ["Sphygmomanometer", "Stethoscope"],
                    "specialization": "General Practice",
                    "accuracy": 0.99,
                    "invasiveness": 1
                },
                {
                    "name": "MRI",
                    "description": "Detailed imaging using magnetic fields and radio waves",
                    "required_equipment": ["MRI Machine"],
                    "specialization": "Radiology",
                    "accuracy": 0.97,
                    "invasiveness": 2
                },
                {
                    "name": "CT Scan",
                    "description": "Cross-sectional imaging using X-rays",
                    "required_equipment": ["CT Scanner"],
                    "specialization": "Radiology",
                    "accuracy": 0.95,
                    "invasiveness": 3
                },
                {
                    "name": "Urinalysis",
                    "description": "Physical, chemical and microscopic analysis of urine",
                    "required_equipment": ["Lab Equipment", "Collection Cup"],
                    "specialization": "General Practice",
                    "accuracy": 0.9,
                    "invasiveness": 1
                }
            ]
            
            for test in tests:
                self.cursor.execute('''
                INSERT INTO diagnostic_tests (
                    name, description, required_equipment, specialization, accuracy, invasiveness
                ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    test["name"],
                    test["description"],
                    json.dumps(test["required_equipment"]),
                    test["specialization"],
                    test["accuracy"],
                    test["invasiveness"]
                ))
            
            print("Initialized diagnostic tests database")
        
        # Check if medications table is empty
        self.cursor.execute("SELECT COUNT(*) as count FROM medications")
        medication_count = self.cursor.fetchone()['count']
        
        if medication_count == 0:
            # Add sample medications
            medications = [
                {
                    "name": "Beta-blockers",
                    "description": "Reduce blood pressure and heart rate",
                    "effects": {
                        "heart_rate": "decrease",
                        "blood_pressure": "decrease"
                    },
                    "side_effects": ["Fatigue", "Cold Hands", "Dizziness"],
                    "specialization": "Cardiology",
                    "dosage": "10-100mg daily"
                },
                {
                    "name": "Antibiotics",
                    "description": "Combat bacterial infections",
                    "effects": {
                        "infection": "decrease",
                        "fever": "decrease"
                    },
                    "side_effects": ["Nausea", "Diarrhea", "Allergic Reaction"],
                    "specialization": "General Practice",
                    "dosage": "Varies by type"
                },
                {
                    "name": "ACE Inhibitors",
                    "description": "Lower blood pressure by relaxing blood vessels",
                    "effects": {
                        "blood_pressure": "decrease"
                    },
                    "side_effects": ["Dry Cough", "Dizziness", "Increased Potassium Levels"],
                    "specialization": "Cardiology",
                    "dosage": "10-40mg daily"
                },
                {
                    "name": "Pain Relief",
                    "description": "Reduces pain perception",
                    "effects": {
                        "pain": "decrease"
                    },
                    "side_effects": ["Drowsiness", "Liver Damage (high doses)", "Stomach Irritation"],
                    "specialization": "General Practice",
                    "dosage": "As needed, follow directions"
                },
                {
                    "name": "Oxygen Therapy",
                    "description": "Supplemental oxygen administration",
                    "effects": {
                        "oxygen_saturation": "increase",
                        "shortness_of_breath": "decrease"
                    },
                    "side_effects": ["Dry Nose", "Headache"],
                    "specialization": "Emergency Medicine",
                    "dosage": "1-15 L/min as needed"
                }
            ]
            
            for med in medications:
                self.cursor.execute('''
                INSERT INTO medications (
                    name, description, effects, side_effects, specialization, dosage
                ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    med["name"],
                    med["description"],
                    json.dumps(med["effects"]),
                    json.dumps(med["side_effects"]),
                    med["specialization"],
                    med["dosage"]
                ))
            
            print("Initialized medications database")
        
        # Check if patients table is empty
        self.cursor.execute("SELECT COUNT(*) as count FROM patients")
        patient_count = self.cursor.fetchone()['count']
        
        if patient_count == 0:
            # Add sample patients from the existing data loader
            from utils.data_loader import DataLoader
            sample_patients = DataLoader.get_sample_patients()
            
            for patient in sample_patients:
                self.save_patient(patient)
            
            print("Initialized patients database")
        
        self.connection.commit()
        print("Sample data initialization complete")


# Initialize the global database instance
db = Database()