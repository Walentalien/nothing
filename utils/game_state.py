import random
import os
from typing import Optional, List, Dict, Any
from datetime import datetime

from models.patient import Patient
from models.doctor import Doctor
from utils.data_loader import DataLoader
from utils.db_manager import DBManager  # Import the PostgreSQL database manager

class GameState:
    """
    Manages the state of the game, including the current doctor, patient,
    game progression, and score.
    """
    
    def __init__(self):
        """Initialize the game state with empty values."""
        self.doctor: Optional[Doctor] = None
        self.current_patient: Optional[Patient] = None
        self.patients: List[Patient] = []
        self.score: int = 0
        self.game_difficulty: str = 'medium'  # 'easy', 'medium', 'hard'
        self.current_level: int = 1
        self.max_levels: int = 10
        self.current_case_id: Optional[str] = None
        self.cases_completed: List[str] = []
        self.session_start_time: datetime = datetime.now()
        
        # Initialize the database and patient data
        self._initialize_patient_data()
    
    def _initialize_patient_data(self) -> None:
        """Initialize patient data from the database or create sample data if not available."""
        # Load patients from the database
        self.patients = DBManager.get_all_patients()
        
        # If no patients in the database, use hardcoded sample patients
        if not self.patients:
            print("No patients found in database, using sample patients")
            self.patients = DataLoader.get_sample_patients()
            
            # Save sample patients to database
            for patient in self.patients:
                DBManager.save_patient(patient)
    
    def set_doctor(self, doctor: Doctor) -> None:
        """
        Set the player's doctor character.
        
        Args:
            doctor: Doctor object representing the player
        """
        self.doctor = doctor
    
    def load_patient(self, patient_id: str) -> bool:
        """
        Load a specific patient by ID from the database.
        
        Args:
            patient_id: Unique identifier for the patient
            
        Returns:
            True if patient was found and loaded, False otherwise
        """
        patient = DBManager.get_patient(patient_id)
        if patient:
            self.current_patient = patient
            self.current_case_id = f"case_{patient_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            return True
        
        # Fallback to memory if not in database
        for patient in self.patients:
            if patient.patient_id == patient_id:
                self.current_patient = patient
                self.current_case_id = f"case_{patient_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                return True
                
        return False
        
    def load_patient_from_db(self, patient_id: str) -> bool:
        """
        Load a patient from the PostgreSQL database by their ID.
        
        Args:
            patient_id: The ID of the patient to load
            
        Returns:
            True if patient was successfully loaded, False otherwise
        """
        try:
            # Get the patient from the database
            db_patient = DBManager.get_patient(patient_id)
            
            if db_patient:
                # Convert database model to domain model if needed
                if hasattr(Patient, 'from_db'):
                    self.current_patient = Patient.from_db(db_patient)
                else:
                    # Use the database model directly
                    self.current_patient = db_patient
                    
                self.current_case_id = f"case_{patient_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                print(f"Loaded patient {self.current_patient.name} from database")
                return True
            else:
                print(f"Patient {patient_id} not found in database")
                # Fall back to loading a random patient
                return self.load_random_patient()
        except Exception as e:
            print(f"Error loading patient from database: {e}")
            # Fall back to loading a random patient
            return self.load_random_patient()
    
    def load_random_patient(self) -> bool:
        """
        Load a random patient from the available patients.
        
        Returns:
            True if a patient was loaded, False if no patients available
        """
        if not self.patients:
            return False
        
        # Choose patient based on difficulty and not previously seen
        available_patients = [p for p in self.patients if p.patient_id not in self.cases_completed]
        
        # If all patients have been seen, reset the completed cases
        if not available_patients:
            self.cases_completed = []
            available_patients = self.patients
        
        # Filter by difficulty
        if self.game_difficulty == 'easy':
            filtered_patients = [p for p in available_patients if p.condition_severity <= 4]
        elif self.game_difficulty == 'hard':
            filtered_patients = [p for p in available_patients if p.condition_severity >= 7]
        else:  # medium
            filtered_patients = [p for p in available_patients if 4 < p.condition_severity < 7]
        
        # Default to all available if filtering resulted in empty list
        if not filtered_patients:
            filtered_patients = available_patients
        
        # Select a random patient
        selected_patient = random.choice(filtered_patients)
        
        # Create a new instance to avoid modifying the template
        self.current_patient = Patient(
            patient_id=f"{selected_patient.patient_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name=selected_patient.name,
            age=selected_patient.age,
            gender=selected_patient.gender,
            medical_history=selected_patient.medical_history.copy(),
            current_symptoms=selected_patient.current_symptoms.copy(),
            vital_signs=selected_patient.vital_signs,  # This creates a new instance
            diagnosis=None,
            condition_severity=selected_patient.condition_severity
        )
        
        # Generate a unique case ID
        self.current_case_id = f"case_{self.current_patient.patient_id}"
        
        return True
    
    def save_current_patient(self) -> bool:
        """
        Save the current patient's state to the database.
        
        Returns:
            True if successful, False otherwise
        """
        if not self.current_patient:
            return False
        
        # Save patient to database
        return DBManager.save_patient(self.current_patient)
    
    def save_test_result(self, test_name: str, results: Dict) -> bool:
        """
        Save a test result to the database.
        
        Args:
            test_name: Name of the test
            results: Test result data
            
        Returns:
            True if successful, False otherwise
        """
        if not self.current_patient:
            return False
        
        return DBManager.save_test_result(self.current_patient.patient_id, test_name, results)
    
    def get_test_results(self, test_name: Optional[str] = None) -> List[Dict]:
        """
        Get test results for the current patient.
        
        Args:
            test_name: Optional test name to filter by
            
        Returns:
            List of test result dictionaries
        """
        if not self.current_patient:
            return []
        
        # Get test results from database
        test_results = []
        for test in self.current_patient.tests_performed:
            if test_name is None or test['test'] == test_name:
                test_results.append(test)
        return test_results
    
    def save_imaging_result(self, image_type: str, image_path: str, description: str) -> bool:
        """
        Save an imaging result for the current patient.
        
        Args:
            image_type: Type of image (X-ray, ECG, etc.)
            image_path: Path to the image file
            description: Description of the findings
            
        Returns:
            True if successful, False otherwise
        """
        if not self.current_patient:
            return False
        
        # Save imaging result using DBManager
        result = DBManager.save_test_result(
            self.current_patient.patient_id,
            image_type,
            {
                'details': {'image_path': image_path},
                'interpretation': description,
                'is_abnormal': False  # Default value, could be updated based on interpretation
            }
        )
        return result
    
    def get_imaging_results(self, image_type: Optional[str] = None) -> List[Dict]:
        """
        Get imaging results for the current patient.
        
        Args:
            image_type: Optional image type to filter by
            
        Returns:
            List of imaging result dictionaries
        """
        if not self.current_patient:
            return []
        
        # Filter tests that have image results
        image_results = []
        for test in self.current_patient.tests_performed:
            if image_type is None or test['test'] == image_type:
                # Check if this test has an image result
                if 'details' in test and 'image_path' in test['details']:
                    image_results.append(test)
        return image_results
    
    def complete_current_case(self) -> None:
        """Mark the current case as completed and save its ID."""
        if self.current_patient:
            patient_template_id = self.current_patient.patient_id.split('_')[0]
            self.cases_completed.append(patient_template_id)
            
            # Save final state of patient
            DBManager.save_patient(self.current_patient)
    
    def advance_level(self) -> bool:
        """
        Advance to the next level of the game.
        
        Returns:
            True if advanced successfully, False if game is completed
        """
        if self.current_level < self.max_levels:
            self.current_level += 1
            
            # Complete the current case if exists
            if self.current_patient:
                self.complete_current_case()
                
            return True
        return False
    
    def set_difficulty(self, difficulty: str) -> None:
        """
        Set the game difficulty.
        
        Args:
            difficulty: Difficulty level ('easy', 'medium', 'hard')
        """
        if difficulty in ['easy', 'medium', 'hard']:
            self.game_difficulty = difficulty
    
    def add_score(self, points: int) -> None:
        """
        Add points to the player's score.
        
        Args:
            points: Number of points to add (can be negative for penalties)
        """
        self.score += points
        if self.score < 0:
            self.score = 0
        
        # Also update doctor's score if exists
        if self.doctor:
            self.doctor.score += points
    
    def reset_game(self) -> None:
        """Reset the game state for a new game."""
        self.score = 0
        self.current_level = 1
        self.current_patient = None
        self.current_case_id = None
        self.cases_completed = []
        self.session_start_time = datetime.now()
        
        # Keep the doctor but reset stats
        if self.doctor:
            self.doctor.patients_treated = 0
            self.doctor.successful_diagnoses = 0
            self.doctor.score = 0
    
    def save_game_state(self) -> dict:
        """
        Save the current game state to a dictionary.
        
        Returns:
            Dictionary with serialized game state
        """
        doctor_dict = self.doctor.to_dict() if self.doctor else None
        
        # Save current patient if exists
        if self.current_patient:
            DBManager.save_patient(self.current_patient)
        
        return {
            'doctor': doctor_dict,
            'score': self.score,
            'game_difficulty': self.game_difficulty,
            'current_level': self.current_level,
            'max_levels': self.max_levels,
            'cases_completed': self.cases_completed,
            'session_start': self.session_start_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the player's performance.
        
        Returns:
            Dictionary with performance metrics
        """
        if not self.doctor:
            return {"error": "No doctor data available"}
        
        # Calculate time played
        time_played = datetime.now() - self.session_start_time
        hours_played = time_played.total_seconds() / 3600
        
        # Calculate success rate
        success_rate = self.doctor.get_success_rate()
        
        # Calculate average score per case
        avg_score = 0
        if len(self.cases_completed) > 0:
            avg_score = self.score / len(self.cases_completed)
        
        return {
            "doctor_name": self.doctor.name,
            "specialization": self.doctor.specialization.name if self.doctor.specialization else "None",
            "score": self.score,
            "cases_completed": len(self.cases_completed),
            "success_rate": success_rate,
            "average_score": avg_score,
            "time_played": f"{time_played.total_seconds() / 60:.1f} minutes",
            "difficulty": self.game_difficulty
        }
