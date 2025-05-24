from typing import Dict, List

class Specialization:
    """
    Represents a medical specialization with its own set of capabilities and expertise.
    """
    def __init__(self, name: str, description: str, available_tests: List[str], available_treatments: List[str]):
        """
        Initialize a medical specialization.
        
        Args:
            name: Name of the specialization (e.g., 'Cardiology')
            description: Brief description of the specialty
            available_tests: List of tests available to this specialty
            available_treatments: List of treatments available to this specialty
        """
        self.name = name
        self.description = description
        self.available_tests = available_tests
        self.available_treatments = available_treatments
    
    def to_dict(self) -> Dict:
        """Convert specialization to dictionary for storage or transmission."""
        return {
            'name': self.name,
            'description': self.description,
            'available_tests': self.available_tests,
            'available_treatments': self.available_treatments
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Specialization':
        """Create a Specialization from dictionary data."""
        return cls(
            name=data.get('name', ''),
            description=data.get('description', ''),
            available_tests=data.get('available_tests', []),
            available_treatments=data.get('available_treatments', [])
        )


class Doctor:
    """
    Represents the player character as a doctor with specialized skills and experience.
    """
    def __init__(self, name: str, specialization: Specialization = None, experience: int = 1):
        """
        Initialize a doctor character.
        
        Args:
            name: Doctor's name
            specialization: Doctor's medical specialization
            experience: Experience level (1-5, with 5 being highest)
        """
        self.name = name
        self.specialization = specialization
        self.experience = max(1, min(5, experience))  # Ensure experience is between 1-5
        self.patients_treated = 0
        self.successful_diagnoses = 0
        self.score = 0
    
    def get_success_rate(self) -> float:
        """Calculate success rate based on diagnoses and patients treated."""
        if self.patients_treated == 0:
            return 0.0
        return (self.successful_diagnoses / self.patients_treated) * 100
    
    def can_perform_test(self, test_name: str) -> bool:
        """Check if the doctor can perform a specific test based on specialization."""
        if not self.specialization:
            return False
        return test_name in self.specialization.available_tests
    
    def can_perform_treatment(self, treatment_name: str) -> bool:
        """Check if the doctor can perform a specific treatment based on specialization."""
        if not self.specialization:
            return False
        return treatment_name in self.specialization.available_treatments
    
    def diagnose_patient(self, correct_diagnosis: bool) -> None:
        """
        Update doctor's statistics after diagnosing a patient.
        
        Args:
            correct_diagnosis: Whether the diagnosis was correct
        """
        self.patients_treated += 1
        if correct_diagnosis:
            self.successful_diagnoses += 1
            self.score += 100 * self.experience  # More points for higher experience
        else:
            self.score -= 50  # Penalty for incorrect diagnosis
    
    def set_specialization(self, specialization: Specialization) -> None:
        """
        Set or change the doctor's specialization.
        
        Args:
            specialization: New specialization to assign
        """
        self.specialization = specialization
    
    def to_dict(self) -> Dict:
        """Convert doctor to dictionary for storage or transmission."""
        specialization_dict = self.specialization.to_dict() if self.specialization else None
        
        return {
            'name': self.name,
            'specialization': specialization_dict,
            'experience': self.experience,
            'patients_treated': self.patients_treated,
            'successful_diagnoses': self.successful_diagnoses,
            'score': self.score
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Doctor':
        """Create a Doctor from dictionary data."""
        specialization = None
        if 'specialization' in data and data['specialization']:
            specialization = Specialization.from_dict(data['specialization'])
        
        doctor = cls(
            name=data.get('name', ''),
            specialization=specialization,
            experience=data.get('experience', 1)
        )
        
        doctor.patients_treated = data.get('patients_treated', 0)
        doctor.successful_diagnoses = data.get('successful_diagnoses', 0)
        doctor.score = data.get('score', 0)
        
        return doctor


# Define standard specializations

def get_available_specializations() -> List[Specialization]:
    """
    Return a list of available medical specializations for the player to choose.
    
    Returns:
        List of Specialization objects
    """
    return [
        Specialization(
            name="General Practice",
            description="Non-specialized medicine focusing on whole-person care. "
                        "Can perform basic examinations and treatments.",
            available_tests=[
                "Physical Examination", "Basic Blood Test", "Vital Signs", 
                "Urinalysis", "Blood Pressure"
            ],
            available_treatments=[
                "Pain Relief", "Antibiotics", "IV Fluids", "Wound Care",
                "Oxygen Therapy"
            ]
        ),
        Specialization(
            name="Cardiology",
            description="Specializes in disorders of the heart and circulatory system. "
                        "Expert in heart-related diagnostics and treatments.",
            available_tests=[
                "ECG/EKG", "Echocardiogram", "Stress Test", "Cardiac Enzyme Test",
                "Blood Pressure", "Cholesterol Panel"
            ],
            available_treatments=[
                "Beta-blockers", "ACE Inhibitors", "Anticoagulants", "Statins",
                "Defibrillation", "CPR"
            ]
        ),
        Specialization(
            name="Neurology",
            description="Focuses on the nervous system including the brain and spinal cord. "
                        "Specializes in neurological disorders and injuries.",
            available_tests=[
                "Neurological Examination", "CT Scan", "MRI", "EEG",
                "Lumbar Puncture", "Reflex Test"
            ],
            available_treatments=[
                "Anticonvulsants", "Pain Management", "Anti-inflammatory Drugs",
                "Physical Therapy Recommendations", "Cognitive Therapy"
            ]
        ),
        Specialization(
            name="Emergency Medicine",
            description="Specializes in acute illnesses and injuries requiring immediate attention. "
                        "Trained to handle a wide variety of emergency situations.",
            available_tests=[
                "Trauma Assessment", "Rapid Blood Tests", "X-Ray", "CT Scan",
                "Toxicology Screen", "Vital Signs Monitoring"
            ],
            available_treatments=[
                "Trauma Care", "Intubation", "Emergency Surgery Preparation",
                "Defibrillation", "Drug Overdose Treatment", "CPR",
                "Blood Transfusion", "Wound Care"
            ]
        )
    ]
