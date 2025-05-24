from typing import Dict, List, Optional, Tuple

class Diagnosis:
    """
    Represents a medical diagnosis with associated symptoms, tests, and treatments.
    """
    def __init__(self, 
                 name: str, 
                 description: str,
                 primary_symptoms: List[str],
                 secondary_symptoms: List[str] = None,
                 recommended_tests: List[str] = None,
                 recommended_treatments: List[str] = None,
                 severity: int = 3  # 1-10 scale
                ):
        """
        Initialize a diagnosis with its characteristics.
        
        Args:
            name: Name of the diagnosis
            description: Brief description of the condition
            primary_symptoms: List of primary symptoms that strongly indicate this diagnosis
            secondary_symptoms: List of secondary symptoms that may be present
            recommended_tests: Tests that help confirm this diagnosis
            recommended_treatments: Treatments typically used for this condition
            severity: How severe this condition typically is (1-10)
        """
        self.name = name
        self.description = description
        self.primary_symptoms = primary_symptoms
        self.secondary_symptoms = secondary_symptoms or []
        self.recommended_tests = recommended_tests or []
        self.recommended_treatments = recommended_treatments or []
        self.severity = max(1, min(10, severity))  # Ensure severity is between 1-10
    
    def to_dict(self) -> Dict:
        """Convert diagnosis to dictionary for storage."""
        return {
            'name': self.name,
            'description': self.description,
            'primary_symptoms': self.primary_symptoms,
            'secondary_symptoms': self.secondary_symptoms,
            'recommended_tests': self.recommended_tests,
            'recommended_treatments': self.recommended_treatments,
            'severity': self.severity
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Diagnosis':
        """Create a Diagnosis from dictionary data."""
        return cls(
            name=data.get('name', ''),
            description=data.get('description', ''),
            primary_symptoms=data.get('primary_symptoms', []),
            secondary_symptoms=data.get('secondary_symptoms', []),
            recommended_tests=data.get('recommended_tests', []),
            recommended_treatments=data.get('recommended_treatments', []),
            severity=data.get('severity', 3)
        )


class DiagnosisManager:
    """
    Manages a catalog of possible diagnoses and provides matching functionality.
    """
    def __init__(self):
        """Initialize the diagnosis manager with a default catalog."""
        self.diagnoses = {}
        self._initialize_catalog()
    
    def _initialize_catalog(self) -> None:
        """Initialize the catalog with common medical diagnoses."""
        diagnosis_list = [
            Diagnosis(
                name="Acute Myocardial Infarction",
                description="Heart attack caused by blocked blood flow to the heart muscle",
                primary_symptoms=["Chest Pain", "Shortness of Breath", "Sweating"],
                secondary_symptoms=["Nausea", "Dizziness", "Fatigue"],
                recommended_tests=["ECG/EKG", "Cardiac Enzyme Test", "Blood Pressure"],
                recommended_treatments=["Aspirin", "Beta-blockers", "ACE Inhibitors", "Anticoagulants", "Oxygen Therapy"],
                severity=9
            ),
            Diagnosis(
                name="Pneumonia",
                description="Infection that inflames air sacs in one or both lungs",
                primary_symptoms=["Cough", "Fever", "Shortness of Breath"],
                secondary_symptoms=["Chest Pain", "Fatigue", "Sweating"],
                recommended_tests=["Chest X-Ray", "Blood Culture", "Sputum Culture", "Basic Blood Test"],
                recommended_treatments=["Antibiotics", "Oxygen Therapy", "IV Fluids"],
                severity=6
            ),
            Diagnosis(
                name="Gastroenteritis",
                description="Inflammation of the stomach and intestines",
                primary_symptoms=["Abdominal Pain", "Nausea", "Diarrhea"],
                secondary_symptoms=["Fever", "Headache", "Loss of Appetite"],
                recommended_tests=["Stool Culture", "Basic Blood Test"],
                recommended_treatments=["IV Fluids", "Antibiotics", "Anti-nausea Medication"],
                severity=4
            ),
            Diagnosis(
                name="Migraine",
                description="Recurring headache that causes moderate to severe pain",
                primary_symptoms=["Headache", "Nausea", "Sensitivity to Light"],
                secondary_symptoms=["Dizziness", "Fatigue", "Visual Disturbances"],
                recommended_tests=["Neurological Examination", "MRI"],
                recommended_treatments=["Pain Relief", "Anti-nausea Medication", "Rest in Dark Room"],
                severity=3
            ),
            Diagnosis(
                name="Hypertensive Crisis",
                description="Severe increase in blood pressure that can lead to organ damage",
                primary_symptoms=["Dizziness", "Headache", "Chest Pain"],
                secondary_symptoms=["Shortness of Breath", "Nausea", "Vision Problems"],
                recommended_tests=["Blood Pressure", "ECG/EKG", "Basic Blood Test"],
                recommended_treatments=["ACE Inhibitors", "Beta-blockers", "IV Fluids"],
                severity=8
            ),
            Diagnosis(
                name="Allergic Reaction",
                description="Immune system response to a substance that's normally harmless",
                primary_symptoms=["Rash", "Itching", "Swelling"],
                secondary_symptoms=["Shortness of Breath", "Dizziness", "Nausea"],
                recommended_tests=["Allergy Test", "Basic Blood Test"],
                recommended_treatments=["Antihistamines", "Corticosteroids", "Epinephrine"],
                severity=5
            ),
            Diagnosis(
                name="Influenza",
                description="Contagious viral infection affecting the respiratory system",
                primary_symptoms=["Fever", "Cough", "Fatigue"],
                secondary_symptoms=["Headache", "Sore Throat", "Body Aches"],
                recommended_tests=["Rapid Influenza Diagnostic Test", "Basic Blood Test"],
                recommended_treatments=["Antiviral Medication", "Pain Relief", "Rest"],
                severity=4
            ),
            Diagnosis(
                name="Appendicitis",
                description="Inflammation of the appendix",
                primary_symptoms=["Abdominal Pain", "Nausea", "Loss of Appetite"],
                secondary_symptoms=["Fever", "Vomiting", "Inability to Pass Gas"],
                recommended_tests=["Physical Examination", "CT Scan", "Urinalysis"],
                recommended_treatments=["Surgery", "IV Fluids", "Antibiotics"],
                severity=7
            ),
            Diagnosis(
                name="Diabetes Mellitus",
                description="Chronic condition affecting how the body processes blood sugar",
                primary_symptoms=["Fatigue", "Increased Thirst", "Frequent Urination"],
                secondary_symptoms=["Weight Loss", "Blurred Vision", "Slow-Healing Sores"],
                recommended_tests=["Blood Glucose Test", "Urinalysis", "A1C Test"],
                recommended_treatments=["Insulin", "Oral Medications", "Diet Management"],
                severity=6
            ),
            Diagnosis(
                name="Bronchitis",
                description="Inflammation of the bronchial tubes in the lungs",
                primary_symptoms=["Cough", "Shortness of Breath", "Chest Discomfort"],
                secondary_symptoms=["Fatigue", "Fever", "Sore Throat"],
                recommended_tests=["Chest X-Ray", "Sputum Culture", "Pulmonary Function Test"],
                recommended_treatments=["Bronchodilators", "Antibiotics", "Rest"],
                severity=4
            )
        ]
        
        # Add diagnoses to the catalog
        for diagnosis in diagnosis_list:
            self.add_diagnosis(diagnosis)
    
    def add_diagnosis(self, diagnosis: Diagnosis) -> None:
        """Add a diagnosis to the catalog."""
        self.diagnoses[diagnosis.name] = diagnosis
    
    def get_diagnosis(self, name: str) -> Optional[Diagnosis]:
        """Get a diagnosis by name."""
        return self.diagnoses.get(name)
    
    def get_all_diagnoses(self) -> List[Diagnosis]:
        """Get all diagnoses in the catalog."""
        return list(self.diagnoses.values())
    
    def match_diagnosis(self, symptoms: List[str], tests_performed: List[str] = None) -> List[Tuple[Diagnosis, float]]:
        """
        Match patient symptoms and test results to potential diagnoses.
        
        Args:
            symptoms: List of patient symptoms
            tests_performed: List of tests that have been performed
            
        Returns:
            List of (diagnosis, confidence) tuples, sorted by confidence (highest first)
        """
        if not symptoms:
            return []
        
        tests_performed = tests_performed or []
        matches = []
        
        for diagnosis in self.diagnoses.values():
            # Calculate symptom match score
            primary_matches = sum(1 for s in diagnosis.primary_symptoms if s in symptoms)
            secondary_matches = sum(1 for s in diagnosis.secondary_symptoms if s in symptoms)
            
            # Calculate test match score
            test_matches = sum(1 for t in diagnosis.recommended_tests if t in tests_performed)
            
            # Weights for different types of matches
            primary_weight = 3.0
            secondary_weight = 1.0
            test_weight = 2.0
            
            # Total possible score
            total_possible = (len(diagnosis.primary_symptoms) * primary_weight +
                             len(diagnosis.secondary_symptoms) * secondary_weight)
            
            if total_possible > 0:
                # Calculate symptom confidence
                symptom_score = (primary_matches * primary_weight + 
                                secondary_matches * secondary_weight)
                symptom_confidence = symptom_score / total_possible
                
                # Calculate test confidence if tests were performed
                test_confidence = 0.0
                if diagnosis.recommended_tests and tests_performed:
                    test_score = test_matches * test_weight
                    test_possible = len(diagnosis.recommended_tests) * test_weight
                    test_confidence = test_score / test_possible
                
                # Calculate overall confidence with more weight on symptoms
                overall_confidence = symptom_confidence * 0.7 + test_confidence * 0.3
                
                # Only include diagnoses with reasonable confidence
                if symptom_confidence > 0.2:
                    matches.append((diagnosis, overall_confidence))
        
        # Sort by confidence (highest first)
        return sorted(matches, key=lambda x: x[1], reverse=True)

# Initialize a global instance for convenience
diagnosis_catalog = DiagnosisManager()