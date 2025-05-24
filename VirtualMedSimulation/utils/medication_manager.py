"""
Local medication manager for VirtualDoctor using SQLite
"""
import json
from datetime import datetime
from models.medication_local import MedicationCatalog, MedicationResponse
from models.database_models import Medication, MedicationRecord
from utils.local_db import Session

class MedicationManager:
    """Manages medications and medication administration for the local SQLite version"""
    
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
            result = []
            for med in medications:
                med_dict = {
                    'id': med.id,
                    'name': med.name,
                    'category': med.category,
                    'description': med.description,
                    'dosages': json.loads(med.dosages) if med.dosages else [],
                    'administration_routes': json.loads(med.administration_routes) if med.administration_routes else [],
                    'indications': json.loads(med.indications) if med.indications else [],
                    'contraindications': json.loads(med.contraindications) if med.contraindications else [],
                    'side_effects': json.loads(med.side_effects) if med.side_effects else [],
                    'interactions': json.loads(med.interactions) if med.interactions else []
                }
                result.append(med_dict)
            return result
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
            if not medication:
                return None
                
            med_dict = {
                'id': medication.id,
                'name': medication.name,
                'category': medication.category,
                'description': medication.description,
                'dosages': json.loads(medication.dosages) if medication.dosages else [],
                'administration_routes': json.loads(medication.administration_routes) if medication.administration_routes else [],
                'indications': json.loads(medication.indications) if medication.indications else [],
                'contraindications': json.loads(medication.contraindications) if medication.contraindications else [],
                'side_effects': json.loads(medication.side_effects) if medication.side_effects else [],
                'interactions': json.loads(medication.interactions) if medication.interactions else []
            }
            return med_dict
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
            
            result = []
            for med in medications:
                med_dict = {
                    'id': med.id,
                    'name': med.name,
                    'category': med.category,
                    'description': med.description,
                    'dosages': json.loads(med.dosages) if med.dosages else [],
                    'administration_routes': json.loads(med.administration_routes) if med.administration_routes else [],
                    'indications': json.loads(med.indications) if med.indications else [],
                    'contraindications': json.loads(med.contraindications) if med.contraindications else [],
                    'side_effects': json.loads(med.side_effects) if med.side_effects else [],
                    'interactions': json.loads(med.interactions) if med.interactions else []
                }
                result.append(med_dict)
            return result
        except Exception as e:
            print(f"Error getting medications by category: {e}")
            return []
        finally:
            if 'session' in locals():
                session.close()
    
    @classmethod
    def administer_medication(cls, patient, medication_name, dosage, route):
        """
        Administer a medication to a patient and record the response
        
        Args:
            patient: The patient object
            medication_name: Name of the medication to administer
            dosage: Dosage to administer
            route: Administration route
            
        Returns:
            Dictionary with administration results
        """
        try:
            session = Session()
            
            # Get the medication from the database
            medication_db = session.query(Medication).filter(Medication.name == medication_name).first()
            if not medication_db:
                print(f"Medication {medication_name} not found")
                return {"success": False, "error": "Medication not found"}
            
            # Create medication model for simulation
            from models.medication_local import Medication as MedicationModel
            
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
            medication_response = MedicationResponse(patient, medication_model, dosage, route)
            response = medication_response.simulate_response()
            
            # Create medication record in database
            medication_record = MedicationRecord(
                patient_id=patient.patient_id,
                medication_id=medication_db.id,
                dosage=dosage,
                administration_route=route,
                effectiveness=response.get('effectiveness', 0.0),
                side_effects_experienced=json.dumps(response.get('side_effects', [])),
                vital_changes=json.dumps(response.get('vital_changes', {})),
                notes=response.get('response_text', '')
            )
            session.add(medication_record)
            session.commit()
            
            # Update patient's vital signs based on medication response
            # Note: We don't modify the patient's vitals directly since that would be handled
            # by the main game logic in a real implementation
            vital_changes = response.get('vital_changes', {})
            if vital_changes and patient.vital_signs:
                # In a real implementation, we would update the vital signs here
                print("Vital sign changes:")
                for vital, change in vital_changes.items():
                    if abs(change) > 0.01:  # Only show significant changes
                        print(f"- {vital}: {'+' if change > 0 else ''}{change:.1f}")
            
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

# Initialize medications when this module is imported
MedicationManager.initialize_medications()