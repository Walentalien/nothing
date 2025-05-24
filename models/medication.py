"""
Medication and drug administration models for VirtualDoctor
"""
from typing import Dict, List, Optional, Tuple
import random
import json

class Medication:
    """Represents a medication that can be administered to patients"""
    
    def __init__(self, 
                name: str,
                category: str,
                description: str,
                dosages: List[str], 
                administration_routes: List[str],
                indications: List[str],
                contraindications: List[str] = None,
                side_effects: List[Dict] = None,
                interactions: List[str] = None):
        """
        Initialize a medication with its properties
        
        Args:
            name: Name of the medication
            category: Type/class of medication (antibiotic, painkiller, etc.)
            description: Brief description of the medication
            dosages: Available dosages
            administration_routes: How the drug can be administered (oral, IV, etc.)
            indications: Conditions this medication is used for
            contraindications: Conditions where this medication shouldn't be used
            side_effects: Possible side effects with their probabilities
            interactions: Other medications this drug interacts with
        """
        self.name = name
        self.category = category
        self.description = description
        self.dosages = dosages
        self.administration_routes = administration_routes
        self.indications = indications
        self.contraindications = contraindications or []
        self.side_effects = side_effects or []
        self.interactions = interactions or []
    
    def to_dict(self) -> Dict:
        """Convert medication to dictionary for storage/serialization"""
        return {
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'dosages': self.dosages,
            'administration_routes': self.administration_routes,
            'indications': self.indications,
            'contraindications': self.contraindications,
            'side_effects': self.side_effects,
            'interactions': self.interactions
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Medication':
        """Create a Medication from dictionary data"""
        return cls(
            name=data['name'],
            category=data['category'],
            description=data['description'],
            dosages=data['dosages'],
            administration_routes=data['administration_routes'],
            indications=data['indications'],
            contraindications=data.get('contraindications', []),
            side_effects=data.get('side_effects', []),
            interactions=data.get('interactions', [])
        )


class MedicationResponse:
    """Simulates a patient's response to medication"""
    
    def __init__(self, patient, medication, dosage, route):
        """
        Initialize a medication response simulator
        
        Args:
            patient: The patient receiving the medication
            medication: The medication being administered
            dosage: The dosage administered
            route: The administration route
        """
        self.patient = patient
        self.medication = medication
        self.dosage = dosage
        self.route = route
        
    def simulate_response(self) -> Dict:
        """
        Simulate the patient's response to the medication
        
        Returns:
            Dictionary with response details
        """
        # Check for effectiveness based on patient's condition and medication indications
        effectiveness = self._calculate_effectiveness()
        
        # Check for side effects
        side_effects = self._simulate_side_effects()
        
        # Calculate vital sign changes
        vital_changes = self._calculate_vital_changes(effectiveness)
        
        # Generate response text
        response_text = self._generate_response_text(effectiveness, side_effects)
        
        return {
            'effectiveness': effectiveness,
            'side_effects': side_effects,
            'vital_changes': vital_changes,
            'response_text': response_text
        }
    
    def _calculate_effectiveness(self) -> float:
        """
        Calculate how effective the medication is for the patient's condition
        
        Returns:
            Effectiveness score between 0.0 (not effective) and 1.0 (very effective)
        """
        # Base effectiveness - moderate
        effectiveness = 0.5
        
        # If the patient has a diagnosis and it's in the medication's indications, increase effectiveness
        if self.patient.diagnosis and any(indication.lower() in self.patient.diagnosis.lower() 
                                        for indication in self.medication.indications):
            effectiveness += 0.3
        
        # If the patient has symptoms matching the medication's indications, increase effectiveness
        symptom_match = False
        for symptom in self.patient.current_symptoms:
            for indication in self.medication.indications:
                if symptom.lower() in indication.lower():
                    symptom_match = True
                    break
        
        if symptom_match:
            effectiveness += 0.2
        
        # If the patient has contraindications, decrease effectiveness
        if any(contraindication.lower() in self.patient.medical_history 
               for contraindication in self.medication.contraindications):
            effectiveness -= 0.4
        
        # Add some randomness (±0.1)
        effectiveness += random.uniform(-0.1, 0.1)
        
        # Ensure effectiveness is between 0 and 1
        return max(0.0, min(1.0, effectiveness))
    
    def _simulate_side_effects(self) -> List[Dict]:
        """
        Simulate whether the patient experiences side effects
        
        Returns:
            List of side effects experienced
        """
        experienced_effects = []
        
        for effect in self.medication.side_effects:
            # Each side effect has a probability, check if it occurs
            probability = effect.get('probability', 0.1)
            
            # Adjust probability based on patient factors
            # For example, elderly patients might be more susceptible
            if self.patient.age > 65:
                probability *= 1.5
            
            # Check if side effect occurs
            if random.random() < probability:
                experienced_effects.append({
                    'name': effect['name'],
                    'severity': effect.get('severity', random.choice(['mild', 'moderate', 'severe']))
                })
        
        return experienced_effects
    
    def _calculate_vital_changes(self, effectiveness: float) -> Dict:
        """
        Calculate changes to the patient's vital signs based on medication response
        
        Args:
            effectiveness: How effective the medication is (0.0-1.0)
            
        Returns:
            Dictionary of vital sign changes
        """
        # Initialize with no changes
        vital_changes = {
            'pulse': 0,
            'systolic_bp': 0,
            'diastolic_bp': 0,
            'temperature': 0,
            'respiratory_rate': 0,
            'oxygen_saturation': 0
        }
        
        # Simulate medication effects on vitals based on category
        if self.medication.category.lower() == 'painkiller':
            # Painkillers might reduce temperature and pulse slightly
            vital_changes['temperature'] = -0.2 * effectiveness
            vital_changes['pulse'] = -5 * effectiveness
        
        elif self.medication.category.lower() == 'antibiotic':
            # Effective antibiotics reduce fever over time
            if 'fever' in [s.lower() for s in self.patient.current_symptoms]:
                vital_changes['temperature'] = -0.5 * effectiveness
            
        elif self.medication.category.lower() == 'antihypertensive':
            # Blood pressure medications reduce BP
            vital_changes['systolic_bp'] = -15 * effectiveness
            vital_changes['diastolic_bp'] = -10 * effectiveness
            
        elif self.medication.category.lower() == 'bronchodilator':
            # Respiratory medications improve oxygen saturation and respiration
            vital_changes['oxygen_saturation'] = 3 * effectiveness
            vital_changes['respiratory_rate'] = -2 * effectiveness if self.patient.vital_signs.respiratory_rate > 16 else 0
        
        # Add slight randomness to make it more realistic
        for key in vital_changes:
            vital_changes[key] += random.uniform(-0.2, 0.2) * abs(vital_changes[key])
        
        return vital_changes
    
    def _generate_response_text(self, effectiveness: float, side_effects: List[Dict]) -> str:
        """
        Generate a textual description of the patient's response
        
        Args:
            effectiveness: How effective the medication is
            side_effects: List of side effects experienced
            
        Returns:
            Text description of the patient's response
        """
        if effectiveness > 0.8:
            response = f"The patient responds very well to {self.medication.name}. "
            response += "Symptoms are significantly improving."
        elif effectiveness > 0.5:
            response = f"The patient shows moderate improvement after receiving {self.medication.name}. "
        elif effectiveness > 0.2:
            response = f"The patient shows slight improvement after receiving {self.medication.name}. "
        else:
            response = f"The patient shows minimal response to {self.medication.name}. "
        
        # Add information about side effects
        if side_effects:
            response += "\n\nThe following side effects were observed:\n"
            for effect in side_effects:
                response += f"- {effect['name']} ({effect['severity']})\n"
        else:
            response += "\nNo side effects observed."
            
        return response


class MedicationCatalog:
    """Manages a catalog of available medications"""
    
    def __init__(self):
        """Initialize the medication catalog with a default set of medications"""
        self.medications = {}
        self._initialize_catalog()
    
    def _initialize_catalog(self):
        """Initialize the catalog with default medications"""
        # Define some standard medications
        self.add_medication(Medication(
            name="Amoxicillin",
            category="Antibiotic",
            description="Broad-spectrum penicillin antibiotic used to treat bacterial infections.",
            dosages=["250mg", "500mg", "875mg"],
            administration_routes=["Oral"],
            indications=["Respiratory infections", "Ear infections", "Sinusitis", "Pneumonia"],
            contraindications=["Penicillin allergy"],
            side_effects=[
                {"name": "Diarrhea", "probability": 0.15, "severity": "mild"},
                {"name": "Nausea", "probability": 0.1, "severity": "mild"},
                {"name": "Rash", "probability": 0.05, "severity": "moderate"},
                {"name": "Allergic reaction", "probability": 0.01, "severity": "severe"}
            ],
            interactions=["Probenecid", "Allopurinol"]
        ))
        
        self.add_medication(Medication(
            name="Ibuprofen",
            category="Painkiller",
            description="Nonsteroidal anti-inflammatory drug (NSAID) used to reduce pain, inflammation, and fever.",
            dosages=["200mg", "400mg", "600mg", "800mg"],
            administration_routes=["Oral"],
            indications=["Pain", "Inflammation", "Fever", "Headache", "Arthritis"],
            contraindications=["NSAID allergy", "Stomach ulcers", "Heart failure"],
            side_effects=[
                {"name": "Stomach upset", "probability": 0.2, "severity": "mild"},
                {"name": "Heartburn", "probability": 0.15, "severity": "mild"},
                {"name": "Dizziness", "probability": 0.05, "severity": "moderate"},
                {"name": "Stomach bleeding", "probability": 0.01, "severity": "severe"}
            ],
            interactions=["Aspirin", "Blood thinners", "Diuretics"]
        ))
        
        self.add_medication(Medication(
            name="Lisinopril",
            category="Antihypertensive",
            description="ACE inhibitor used to treat high blood pressure and heart failure.",
            dosages=["5mg", "10mg", "20mg", "40mg"],
            administration_routes=["Oral"],
            indications=["Hypertension", "Heart failure", "Post-heart attack"],
            contraindications=["Pregnancy", "History of angioedema"],
            side_effects=[
                {"name": "Dry cough", "probability": 0.2, "severity": "moderate"},
                {"name": "Dizziness", "probability": 0.15, "severity": "mild"},
                {"name": "Low blood pressure", "probability": 0.1, "severity": "moderate"},
                {"name": "Increased potassium", "probability": 0.05, "severity": "moderate"}
            ],
            interactions=["Potassium supplements", "NSAIDs", "Diuretics"]
        ))
        
        self.add_medication(Medication(
            name="Albuterol",
            category="Bronchodilator",
            description="Bronchodilator that relaxes muscles in the airways to improve breathing.",
            dosages=["90mcg inhaler", "2mg tablet", "4mg tablet"],
            administration_routes=["Inhalation", "Oral"],
            indications=["Asthma", "COPD", "Bronchitis", "Wheezing"],
            contraindications=["Tachycardia"],
            side_effects=[
                {"name": "Tremors", "probability": 0.2, "severity": "mild"},
                {"name": "Increased heart rate", "probability": 0.15, "severity": "moderate"},
                {"name": "Nervousness", "probability": 0.1, "severity": "mild"},
                {"name": "Headache", "probability": 0.1, "severity": "mild"}
            ],
            interactions=["Beta-blockers", "Diuretics", "Other stimulants"]
        ))
        
        self.add_medication(Medication(
            name="Metformin",
            category="Antidiabetic",
            description="Oral diabetes medication that helps control blood sugar levels.",
            dosages=["500mg", "850mg", "1000mg"],
            administration_routes=["Oral"],
            indications=["Type 2 diabetes", "Insulin resistance", "Prediabetes"],
            contraindications=["Kidney disease", "Liver disease"],
            side_effects=[
                {"name": "Digestive issues", "probability": 0.3, "severity": "mild"},
                {"name": "Nausea", "probability": 0.2, "severity": "mild"},
                {"name": "Vitamin B12 deficiency", "probability": 0.05, "severity": "moderate"},
                {"name": "Lactic acidosis", "probability": 0.01, "severity": "severe"}
            ],
            interactions=["Contrast dyes", "Alcohol", "Other diabetes medications"]
        ))
    
    def add_medication(self, medication: Medication):
        """Add a medication to the catalog"""
        self.medications[medication.name] = medication
    
    def get_medication(self, name: str) -> Optional[Medication]:
        """Get a medication by name"""
        return self.medications.get(name)
    
    def get_all_medications(self) -> List[Medication]:
        """Get all medications in the catalog"""
        return list(self.medications.values())
    
    def get_medications_by_category(self, category: str) -> List[Medication]:
        """Get all medications in a specific category"""
        return [med for med in self.medications.values() if med.category.lower() == category.lower()]
    
    def get_medications_for_symptom(self, symptom: str) -> List[Medication]:
        """Get all medications that can treat a specific symptom"""
        matching_meds = []
        for med in self.medications.values():
            for indication in med.indications:
                if symptom.lower() in indication.lower():
                    matching_meds.append(med)
                    break
        return matching_meds
    
    def to_dict(self) -> Dict:
        """Convert the catalog to a dictionary for serialization"""
        return {name: med.to_dict() for name, med in self.medications.items()}
    
    def save_to_file(self, filename: str):
        """Save the medication catalog to a JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'MedicationCatalog':
        """Load a medication catalog from a JSON file"""
        catalog = cls()
        catalog.medications = {}  # Clear existing medications
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
            for name, med_data in data.items():
                catalog.add_medication(Medication.from_dict(med_data))
                
            return catalog
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, return default catalog
            return cls()


# Create a global instance of the medication catalog for easy access
medication_catalog = MedicationCatalog()