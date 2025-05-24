from typing import Dict, List, Optional

class Symptom:
    """
    Represents a medical symptom with its characteristics and associations with conditions.
    """
    def __init__(self, 
                 name: str, 
                 description: str, 
                 severity: int = 1,  # 1-5 scale, 5 being most severe
                 body_part: Optional[str] = None,
                 associated_conditions: List[str] = None):
        """
        Initialize a symptom with its basic information.
        
        Args:
            name: Name of the symptom
            description: Description of how the symptom presents
            severity: How severe the symptom is (1-5)
            body_part: Part of the body affected
            associated_conditions: Medical conditions commonly associated with this symptom
        """
        self.name = name
        self.description = description
        self.severity = max(1, min(5, severity))  # Ensure severity is between 1-5
        self.body_part = body_part
        self.associated_conditions = associated_conditions or []
    
    def to_dict(self) -> Dict:
        """Convert symptom to dictionary for storage or transmission."""
        return {
            'name': self.name,
            'description': self.description,
            'severity': self.severity,
            'body_part': self.body_part,
            'associated_conditions': self.associated_conditions
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Symptom':
        """Create a Symptom from dictionary data."""
        return cls(
            name=data.get('name', ''),
            description=data.get('description', ''),
            severity=data.get('severity', 1),
            body_part=data.get('body_part', None),
            associated_conditions=data.get('associated_conditions', [])
        )


class SymptomManager:
    """
    Manages and provides access to a catalog of symptoms.
    """
    def __init__(self):
        """Initialize the symptom manager with a default symptom catalog."""
        self.symptoms = {}
        self._initialize_catalog()
    
    def _initialize_catalog(self) -> None:
        """Initialize the catalog with common symptoms."""
        # This is a basic catalog to start with - will be expanded later
        symptom_list = [
            Symptom(
                name="Chest Pain",
                description="Pain or discomfort in the chest area, possibly radiating to arms, back, or jaw",
                severity=4,
                body_part="Chest",
                associated_conditions=["Heart Attack", "Angina", "Pulmonary Embolism", "Anxiety"]
            ),
            Symptom(
                name="Shortness of Breath",
                description="Difficulty breathing or feeling like you can't get enough air",
                severity=4,
                body_part="Lungs",
                associated_conditions=["Asthma", "COPD", "Heart Failure", "Pneumonia", "Anxiety"]
            ),
            Symptom(
                name="Headache",
                description="Pain in the head or upper neck area",
                severity=3,
                body_part="Head",
                associated_conditions=["Migraine", "Tension Headache", "Concussion", "Meningitis", "Stroke"]
            ),
            Symptom(
                name="Nausea",
                description="Feeling of discomfort in the stomach with an urge to vomit",
                severity=2,
                body_part="Stomach",
                associated_conditions=["Food Poisoning", "Migraine", "Pregnancy", "Motion Sickness", "Infection"]
            ),
            Symptom(
                name="Fever",
                description="Elevated body temperature above the normal range",
                severity=3,
                body_part="Whole Body",
                associated_conditions=["Infection", "Inflammation", "Heat Exhaustion", "Malignancy"]
            ),
            Symptom(
                name="Fatigue",
                description="Feeling of extreme tiredness, lacking energy",
                severity=2,
                body_part="Whole Body",
                associated_conditions=["Anemia", "Depression", "Chronic Fatigue Syndrome", "Sleep Disorders", "Infection"]
            ),
            Symptom(
                name="Dizziness",
                description="Sensation of spinning or lightheadedness",
                severity=3,
                body_part="Head",
                associated_conditions=["Vertigo", "Low Blood Pressure", "Anemia", "Dehydration", "Anxiety"]
            ),
            Symptom(
                name="Cough",
                description="Sudden expulsion of air from the lungs",
                severity=2,
                body_part="Lungs",
                associated_conditions=["Common Cold", "Bronchitis", "Pneumonia", "Asthma", "Allergies"]
            ),
            Symptom(
                name="Abdominal Pain",
                description="Pain felt between the chest and pelvic regions",
                severity=3,
                body_part="Abdomen",
                associated_conditions=["Appendicitis", "Gastritis", "IBS", "Kidney Stones", "Food Poisoning"]
            ),
            Symptom(
                name="Rash",
                description="Skin eruption or discoloration",
                severity=2,
                body_part="Skin",
                associated_conditions=["Allergic Reaction", "Eczema", "Psoriasis", "Infection", "Drug Reaction"]
            )
        ]
        
        # Add symptoms to the catalog
        for symptom in symptom_list:
            self.add_symptom(symptom)
    
    def add_symptom(self, symptom: Symptom) -> None:
        """Add a symptom to the catalog."""
        self.symptoms[symptom.name] = symptom
    
    def get_symptom(self, name: str) -> Optional[Symptom]:
        """Get a symptom by name."""
        return self.symptoms.get(name)
    
    def get_all_symptoms(self) -> List[Symptom]:
        """Get all symptoms in the catalog."""
        return list(self.symptoms.values())
    
    def get_symptoms_by_body_part(self, body_part: str) -> List[Symptom]:
        """Get all symptoms associated with a specific body part."""
        return [symptom for symptom in self.symptoms.values() if symptom.body_part == body_part]
    
    def get_symptoms_by_condition(self, condition: str) -> List[Symptom]:
        """Get all symptoms associated with a specific medical condition."""
        return [
            symptom for symptom in self.symptoms.values() 
            if condition in symptom.associated_conditions
        ]

# Initialize a global instance for convenience
symptom_catalog = SymptomManager()
