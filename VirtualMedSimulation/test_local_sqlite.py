"""
Test SQLite implementation for VirtualDoctor
"""
import os
import sys
import json
from datetime import datetime

# Make sure local modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import local database setup
from utils.local_db import init_db, Session
from models.database_models import Base, Patient, Medication, MedicationRecord
from models.medication_local import MedicationCatalog
from utils.medication_manager import MedicationManager

def test_sqlite_database():
    """Test the SQLite database implementation"""
    print("Testing SQLite database implementation...")
    
    # Initialize the database
    init_db()
    
    # Create session
    session = Session()
    
    try:
        # Check if medications exist
        med_count = session.query(Medication).count()
        print(f"Found {med_count} medications in database")
        
        if med_count == 0:
            print("Initializing medications...")
            MedicationManager.initialize_medications()
            med_count = session.query(Medication).count()
            print(f"Now have {med_count} medications in database")
        
        # Get all medications
        medications = MedicationManager.get_all_medications()
        print(f"Retrieved {len(medications)} medications from database")
        
        # Get medications by category
        antibiotics = MedicationManager.get_medications_by_category("Antibiotic")
        print(f"Found {len(antibiotics)} antibiotics")
        
        painkillers = MedicationManager.get_medications_by_category("Painkiller")
        print(f"Found {len(painkillers)} painkillers")
        
        # Create a test patient
        from collections import namedtuple
        
        # Create a VitalSigns namedtuple
        VitalSigns = namedtuple('VitalSigns', [
            'pulse', 'systolic_bp', 'diastolic_bp', 
            'temperature', 'respiratory_rate', 'oxygen_saturation'
        ])
        
        # Create a TestPatient class
        class TestPatient:
            def __init__(self):
                self.patient_id = f"TEST{datetime.now().strftime('%Y%m%d%H%M%S')}"
                self.name = "Test Patient"
                self.age = 45
                self.gender = "Male"
                self.medical_history = ["Hypertension", "Asthma"]
                self.current_symptoms = ["Fever", "Cough", "Chest pain"]
                self.diagnosis = None
                self.condition_severity = 2
                vital_signs = VitalSigns(
                    pulse=88, 
                    systolic_bp=140, 
                    diastolic_bp=90, 
                    temperature=38.2, 
                    respiratory_rate=18, 
                    oxygen_saturation=96
                )
                self.vital_signs = vital_signs
                
            # Allow mutable vital signs for medication effects
            @property
            def pulse(self):
                return self.vital_signs.pulse
                
            @property
            def systolic_bp(self):
                return self.vital_signs.systolic_bp
                
            @property
            def diastolic_bp(self):
                return self.vital_signs.diastolic_bp
                
            @property
            def temperature(self):
                return self.vital_signs.temperature
                
            @property
            def respiratory_rate(self):
                return self.vital_signs.respiratory_rate
                
            @property
            def oxygen_saturation(self):
                return self.vital_signs.oxygen_saturation
        
        test_patient = TestPatient()
        print(f"Created test patient: {test_patient.name} (ID: {test_patient.patient_id})")
        
        # Test administering medication
        if medications:
            print("\nTesting medication administration:")
            med_name = medications[0]['name']
            dosage = medications[0]['dosages'][0]
            route = medications[0]['administration_routes'][0]
            
            print(f"Administering {med_name} {dosage} {route} to patient...")
            result = MedicationManager.administer_medication(
                test_patient,
                med_name,
                dosage,
                route
            )
            
            if result['success']:
                print("Medication administered successfully!")
                print(f"Effectiveness: {result['effectiveness']:.2f}")
                if result['side_effects']:
                    print("Side effects:")
                    for effect in result['side_effects']:
                        print(f"- {effect['name']} ({effect['severity']})")
                
                if result['vital_changes']:
                    print("Vital sign changes:")
                    for vital, change in result['vital_changes'].items():
                        if abs(change) > 0.01:
                            print(f"- {vital}: {'+' if change > 0 else ''}{change:.1f}")
                
                print("\nPatient response:")
                print(result['response_text'])
            else:
                print(f"Error: {result['error']}")
        
        print("\nDatabase test completed successfully!")
        
    except Exception as e:
        print(f"Error during database test: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    test_sqlite_database()