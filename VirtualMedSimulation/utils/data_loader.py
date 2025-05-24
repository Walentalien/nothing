import json
import os
import random
from typing import List, Dict, Optional

from models.patient import Patient, VitalSigns

class DataLoader:
    """
    Utility class for loading patient data from JSON files or database.
    """
    
    @staticmethod
    def load_patients_from_json(file_path: str) -> List[Patient]:
        """
        Load patient data from a JSON file.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            List of Patient objects
        """
        patients = []
        
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                
                if 'patients' in data:
                    for patient_data in data['patients']:
                        try:
                            patient = Patient.from_dict(patient_data)
                            patients.append(patient)
                        except Exception as e:
                            print(f"Error loading patient: {e}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except json.JSONDecodeError:
            print(f"Invalid JSON format in file: {file_path}")
        except Exception as e:
            print(f"Error loading patients from JSON: {e}")
        
        return patients
    
    @staticmethod
    def get_sample_patients() -> List[Patient]:
        """
        Generate a list of sample patients for testing or when no data file is available.
        
        Returns:
            List of sample Patient objects
        """
        sample_patients = [
            Patient(
                patient_id="P001",
                name="John Smith",
                age=45,
                gender="Male",
                medical_history=["Hypertension", "High Cholesterol"],
                current_symptoms=["Chest Pain", "Shortness of Breath", "Sweating"],
                vital_signs=VitalSigns(
                    pulse=110,
                    systolic_bp=160,
                    diastolic_bp=95,
                    temperature=37.2,
                    respiratory_rate=22,
                    oxygen_saturation=94
                ),
                condition_severity=7
            ),
            Patient(
                patient_id="P002",
                name="Sarah Johnson",
                age=32,
                gender="Female",
                medical_history=["Asthma"],
                current_symptoms=["Cough", "Fever", "Fatigue"],
                vital_signs=VitalSigns(
                    pulse=95,
                    systolic_bp=125,
                    diastolic_bp=80,
                    temperature=38.7,
                    respiratory_rate=20,
                    oxygen_saturation=96
                ),
                condition_severity=4
            ),
            Patient(
                patient_id="P003",
                name="Robert Davis",
                age=67,
                gender="Male",
                medical_history=["Diabetes Type 2", "Coronary Artery Disease", "Stroke (2018)"],
                current_symptoms=["Dizziness", "Confusion", "Headache"],
                vital_signs=VitalSigns(
                    pulse=88,
                    systolic_bp=175,
                    diastolic_bp=100,
                    temperature=36.5,
                    respiratory_rate=18,
                    oxygen_saturation=95
                ),
                condition_severity=6
            ),
            Patient(
                patient_id="P004",
                name="Emily Wilson",
                age=28,
                gender="Female",
                medical_history=[],
                current_symptoms=["Abdominal Pain", "Nausea", "Loss of Appetite"],
                vital_signs=VitalSigns(
                    pulse=100,
                    systolic_bp=110,
                    diastolic_bp=70,
                    temperature=37.8,
                    respiratory_rate=16,
                    oxygen_saturation=98
                ),
                condition_severity=3
            ),
            Patient(
                patient_id="P005",
                name="Michael Chen",
                age=52,
                gender="Male",
                medical_history=["Allergies to Penicillin"],
                current_symptoms=["Rash", "Itching", "Swelling"],
                vital_signs=VitalSigns(
                    pulse=105,
                    systolic_bp=135,
                    diastolic_bp=85,
                    temperature=37.4,
                    respiratory_rate=18,
                    oxygen_saturation=97
                ),
                condition_severity=2
            )
        ]
        
        return sample_patients
    
    @staticmethod
    def save_patients_to_json(patients: List[Patient], file_path: str) -> bool:
        """
        Save a list of patients to a JSON file.
        
        Args:
            patients: List of Patient objects to save
            file_path: Path where the JSON file will be saved
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert patients to dictionaries
            patient_dicts = []
            for patient in patients:
                # Convert vital signs to dict
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
                
                # Create patient dict
                patient_dict = {
                    'patient_id': patient.patient_id,
                    'name': patient.name,
                    'age': patient.age,
                    'gender': patient.gender,
                    'medical_history': patient.medical_history,
                    'current_symptoms': patient.current_symptoms,
                    'vital_signs': vital_signs_dict,
                    'diagnosis': patient.diagnosis,
                    'condition_severity': patient.condition_severity
                }
                
                patient_dicts.append(patient_dict)
            
            # Save to file
            with open(file_path, 'w') as file:
                json.dump({'patients': patient_dicts}, file, indent=4)
            
            return True
        except Exception as e:
            print(f"Error saving patients to JSON: {e}")
            return False
    
    @classmethod
    def initialize_sample_data(cls) -> None:
        """
        Initialize the sample patient data file if it doesn't exist.
        """
        sample_data_path = os.path.join('data', 'sample_patients.json')
        
        # Check if the directory exists, create it if not
        os.makedirs(os.path.dirname(sample_data_path), exist_ok=True)
        
        # Check if the file exists
        if not os.path.exists(sample_data_path):
            # Generate sample patients
            sample_patients = cls.get_sample_patients()
            
            # Save them to file
            cls.save_patients_to_json(sample_patients, sample_data_path)
            print(f"Sample patient data created at {sample_data_path}")
