import os
import random
import sys
from models.doctor import Doctor, get_available_specializations
from models.patient import Patient, VitalSigns
from models.diagnosis import Diagnosis, DiagnosisManager, diagnosis_catalog
from utils.data_loader import DataLoader
from utils.game_state import GameState

def clear_screen():
    """Clear the terminal screen."""
    os.system('clear' if os.name == 'posix' else 'cls')

class ConsoleVirtualDoctor:
    """
    A console-based version of the VirtualDoctor game that works in any Python environment.
    This simplified version maintains core game functionality while bypassing Kivy's graphics requirements.
    """
    
    def __init__(self):
        """Initialize the game with a GameState and load initial data."""
        self.game_state = GameState()
        self.running = True
    
    def display_main_menu(self):
        """Display the main menu options."""
        clear_screen()
        print("\n===== VIRTUAL DOCTOR =====")
        print("Medical Simulation Game")
        print("\n1. Start Doctor Mode")
        print("2. About")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            self.display_specialization_selection()
        elif choice == '2':
            self.display_about()
        elif choice == '3':
            self.running = False
        else:
            input("\nInvalid choice. Press Enter to continue...")
    
    def display_about(self):
        """Display information about the game."""
        clear_screen()
        print("\n===== ABOUT VIRTUAL DOCTOR =====")
        print("\nVirtualDoctor is an educational medical simulation game where")
        print("players take on the role of a doctor, diagnose and treat")
        print("virtual patients in real-time.")
        print("\nDeveloped as a learning tool for medical students and healthcare professionals.")
        print("\n© 2024 VirtualDoctor Team")
        
        input("\nPress Enter to return to the main menu...")
    
    def display_specialization_selection(self):
        """Display the specialization selection screen."""
        clear_screen()
        specializations = get_available_specializations()
        
        print("\n===== SELECT YOUR SPECIALIZATION =====")
        print("Choose a medical specialty that determines your available tests and treatments")
        
        for i, spec in enumerate(specializations, 1):
            print(f"\n{i}. {spec.name}")
            print(f"   {spec.description}")
            print(f"   Tests: {', '.join(spec.available_tests[:3])}...")
            print(f"   Treatments: {', '.join(spec.available_treatments[:3])}...")
        
        print(f"\n{len(specializations) + 1}. Back to Main Menu")
        
        try:
            choice = int(input("\nEnter your choice: "))
            
            if 1 <= choice <= len(specializations):
                selected_spec = specializations[choice - 1]
                
                # Create a doctor with the selected specialization
                self.game_state.doctor = Doctor(name="Dr. Player", specialization=selected_spec)
                
                # Load a random patient
                self.game_state.load_random_patient()
                
                self.display_patient_view()
            elif choice == len(specializations) + 1:
                return  # Back to main menu
            else:
                input("\nInvalid choice. Press Enter to continue...")
        except ValueError:
            input("\nPlease enter a number. Press Enter to continue...")
    
    def display_patient_view(self):
        """Display the patient view screen with vital signs and options."""
        while True:
            clear_screen()
            patient = self.game_state.current_patient
            doctor = self.game_state.doctor
            
            if not patient or not doctor:
                print("Error: No patient or doctor loaded.")
                input("Press Enter to return to the main menu...")
                return
            
            # Display patient information
            print("\n===== PATIENT INFORMATION =====")
            print(f"Name: {patient.name}")
            print(f"Age/Gender: {patient.age} years, {patient.gender}")
            history_text = ", ".join(patient.medical_history) if patient.medical_history else "No significant history"
            print(f"Medical History: {history_text}")
            
            # Display condition severity
            condition_text = "Stable"
            if patient.condition_severity >= 8:
                condition_text = "Critical"
            elif patient.condition_severity >= 5:
                condition_text = "Serious"
            elif patient.condition_severity >= 3:
                condition_text = "Fair"
            print(f"Condition: {condition_text}")
            
            # Display vital signs
            print("\n===== VITAL SIGNS =====")
            print(f"Heart Rate: {patient.vital_signs.pulse} BPM")
            print(f"Blood Pressure: {patient.vital_signs.systolic_bp}/{patient.vital_signs.diastolic_bp} mmHg")
            print(f"Temperature: {patient.vital_signs.temperature:.1f}°C")
            print(f"Respiratory Rate: {patient.vital_signs.respiratory_rate} breaths/min")
            print(f"O₂ Saturation: {patient.vital_signs.oxygen_saturation}%")
            
            # Display symptoms
            print("\n===== SYMPTOMS =====")
            if patient.current_symptoms:
                for symptom in patient.current_symptoms:
                    print(f"• {symptom}")
            else:
                print("No reported symptoms")
            
            # Display actions
            print("\n===== ACTIONS =====")
            print("1. Run Tests")
            print("2. Administer Treatment")
            print("3. Make Diagnosis")
            print("4. Return to Main Menu")
            
            choice = input("\nEnter your choice (1-4): ")
            
            if choice == '1':
                self.display_tests()
            elif choice == '2':
                self.display_treatments()
            elif choice == '3':
                self.display_diagnosis()
            elif choice == '4':
                break
            else:
                input("\nInvalid choice. Press Enter to continue...")
    
    def display_tests(self):
        """Display available tests for the current patient."""
        clear_screen()
        doctor = self.game_state.doctor
        
        print("\n===== AVAILABLE TESTS =====")
        for i, test in enumerate(doctor.specialization.available_tests, 1):
            print(f"{i}. {test}")
        
        print(f"{len(doctor.specialization.available_tests) + 1}. Back")
        
        try:
            choice = int(input("\nEnter your choice: "))
            
            if 1 <= choice <= len(doctor.specialization.available_tests):
                test_name = doctor.specialization.available_tests[choice - 1]
                result = self.game_state.current_patient.perform_test(test_name)
                
                clear_screen()
                print(f"\n===== TEST RESULTS: {test_name} =====")
                print(f"{result['message']}")
                
                # Phase 3: Display detailed test results with imaging
                print("\n----- Details -----")
                
                # Check if there's an image path to display
                image_path = None
                for key, value in result['details'].items():
                    if key == 'image_path':
                        image_path = value
                        print(f"Image generated: {os.path.basename(value)}")
                    else:
                        print(f"{key.replace('_', ' ').title()}: {value}")
                
                print(f"\nInterpretation: {result['interpretation']}")
                
                # Display abnormal flag and recommendations
                if result['is_abnormal']:
                    print("\nNOTE: Abnormal findings detected!")
                
                # Show recommendations if available
                if 'recommendations' in result and result['recommendations']:
                    print("\nRecommendations:")
                    for i, rec in enumerate(result['recommendations'], 1):
                        print(f"  {i}. {rec}")
                        
                # Guide for viewing the image if one was generated
                if image_path:
                    print(f"\nImage saved to: {image_path}")
                    if test_name == "ECG/EKG":
                        print("Note: ECG shows electrical activity of the heart over time.")
                    elif test_name == "Chest X-Ray":
                        print("Note: X-ray shows internal structures of the chest cavity.")
                
                input("\nPress Enter to continue...")
            elif choice == len(doctor.specialization.available_tests) + 1:
                return  # Back to patient view
            else:
                input("\nInvalid choice. Press Enter to continue...")
        except ValueError:
            input("\nPlease enter a number. Press Enter to continue...")
    
    def display_treatments(self):
        """Display available treatments for the current patient."""
        clear_screen()
        doctor = self.game_state.doctor
        
        print("\n===== AVAILABLE TREATMENTS =====")
        for i, treatment in enumerate(doctor.specialization.available_treatments, 1):
            print(f"{i}. {treatment}")
        
        print(f"{len(doctor.specialization.available_treatments) + 1}. Back")
        
        try:
            choice = int(input("\nEnter your choice: "))
            
            if 1 <= choice <= len(doctor.specialization.available_treatments):
                treatment_name = doctor.specialization.available_treatments[choice - 1]
                result = self.game_state.current_patient.apply_treatment(treatment_name)
                
                clear_screen()
                print(f"\n===== TREATMENT APPLIED: {treatment_name} =====")
                print(f"{result['message']}\n")
                
                # Phase 2: Display treatment effects
                if result['effects']:
                    print("----- Effects -----")
                    for effect in result['effects']:
                        print(f"• {effect}")
                    print()
                
                # Display vital sign changes
                if result['vital_changes']:
                    print("----- Vital Sign Changes -----")
                    for vital, change in result['vital_changes'].items():
                        print(f"• {vital.replace('_', ' ').title()}: {change}")
                    print()
                
                input("Press Enter to continue...")
            elif choice == len(doctor.specialization.available_treatments) + 1:
                return  # Back to patient view
            else:
                input("\nInvalid choice. Press Enter to continue...")
        except ValueError:
            input("\nPlease enter a number. Press Enter to continue...")
    
    def display_diagnosis(self):
        """Display diagnosis options for the current patient."""
        clear_screen()
        
        # Phase 2: Get recommended diagnoses based on symptoms and tests
        patient = self.game_state.current_patient
        
        # Extract test names from tests performed
        performed_tests = [test['test'] for test in patient.tests_performed]
        
        # Get diagnostic matches based on symptoms and tests
        diagnostic_matches = diagnosis_catalog.match_diagnosis(
            symptoms=patient.current_symptoms,
            tests_performed=performed_tests
        )
        
        # Get all diagnoses for display
        all_diagnoses = diagnosis_catalog.get_all_diagnoses()
        
        # Sort diagnoses: matched first (by confidence), then alphabetically
        matched_names = [d[0].name for d in diagnostic_matches]
        non_matched = [d for d in all_diagnoses if d.name not in matched_names]
        non_matched.sort(key=lambda x: x.name)
        
        # Print all available diagnoses
        print("\n===== MAKE DIAGNOSIS =====")
        print("Based on symptoms and test results, consider these possibilities:")
        
        i = 1
        # First show matched diagnoses with confidence levels
        for diagnosis, confidence in diagnostic_matches:
            confidence_pct = int(confidence * 100)
            print(f"{i}. {diagnosis.name} (Match confidence: {confidence_pct}%)")
            i += 1
        
        # Then show other diagnoses
        for diagnosis in non_matched:
            print(f"{i}. {diagnosis.name}")
            i += 1
        
        print(f"{len(all_diagnoses) + 1}. Back")
        
        try:
            choice = int(input("\nEnter your choice: "))
            
            if 1 <= choice <= len(all_diagnoses):
                # Get the selected diagnosis
                if choice <= len(diagnostic_matches):
                    selected_diagnosis = diagnostic_matches[choice - 1][0]
                    confidence = diagnostic_matches[choice - 1][1]
                else:
                    idx = choice - len(diagnostic_matches) - 1
                    selected_diagnosis = non_matched[idx]
                    confidence = 0.0
                
                # Check if diagnosis is correct
                # For Phase 2, we consider a diagnosis correct if confidence > 0.6
                # or if it's the highest confidence diagnosis
                is_correct = confidence > 0.6
                if diagnostic_matches and selected_diagnosis.name == diagnostic_matches[0][0].name:
                    is_correct = True
                
                # Update doctor's statistics
                self.game_state.doctor.diagnose_patient(is_correct)
                
                # Set the diagnosis on the patient
                self.game_state.current_patient.diagnosis = selected_diagnosis.name
                
                # Display the diagnosis results
                clear_screen()
                print(f"\n===== DIAGNOSIS MADE: {selected_diagnosis.name} =====")
                print(f"{selected_diagnosis.description}\n")
                
                if is_correct:
                    print("Your diagnosis appears to be accurate based on the patient's symptoms and test results.")
                    # Improve patient condition due to correct diagnosis
                    self.game_state.current_patient.update_condition(-2)
                else:
                    print("Your diagnosis may not fully align with the patient's symptoms and test results.")
                    # Worsen patient condition slightly due to incorrect diagnosis
                    self.game_state.current_patient.update_condition(1)
                
                print("\n----- Recommended Actions -----")
                if selected_diagnosis.recommended_tests:
                    print("Recommended tests:")
                    for test in selected_diagnosis.recommended_tests:
                        status = "✓" if test in performed_tests else " "
                        print(f" {status} {test}")
                
                if selected_diagnosis.recommended_treatments:
                    print("\nRecommended treatments:")
                    for treatment in selected_diagnosis.recommended_treatments:
                        print(f" • {treatment}")
                
                print(f"\nCurrent score: {self.game_state.doctor.score}")
                
                input("\nPress Enter to continue...")
            elif choice == len(all_diagnoses) + 1:
                return  # Back to patient view
            else:
                input("\nInvalid choice. Press Enter to continue...")
        except ValueError:
            input("\nPlease enter a number. Press Enter to continue...")
    
    def run(self):
        """Run the main game loop."""
        while self.running:
            self.display_main_menu()

# Run the appropriate version based on environment
if __name__ == '__main__':
    import os
    from flask import Flask, render_template_string

    if os.environ.get('REPL_SLUG'):  # We're in deployment
        app = Flask(__name__)
        
        @app.route('/')
        def home():
            return render_template_string("""
                <html>
                <head>
                    <title>VirtualDoctor</title>
                    <style>
                        body { font-family: Arial; max-width: 800px; margin: 20px auto; padding: 20px; }
                        h1 { color: #2c3e50; }
                        .info { background: #f8f9fa; padding: 20px; border-radius: 5px; }
                    </style>
                </head>
                <body>
                    <h1>VirtualDoctor - Medical Simulation Game</h1>
                    <div class="info">
                        <p>This is a console-based medical simulation game that requires interactive input.</p>
                        <p>To play the game, please run the application using the appropriate command for your environment.</p>
                        <h2>Game Features</h2>
                        <ul>
                            <li>Choose your medical specialization</li>
                            <li>Diagnose and treat virtual patients</li>
                            <li>Practice medical decision making</li>
                            <li>Learn about different conditions and treatments</li>
                        </ul>
                    </div>
                </body>
                </html>
            """)
        
        app.run(host='0.0.0.0', port=5000)
    else:  # We're in development/console mode
        game = ConsoleVirtualDoctor()
        game.run()
