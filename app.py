from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
import random
from models.doctor import Doctor, get_available_specializations
from models.patient import Patient, VitalSigns
from utils.data_loader import DataLoader

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize sample patient data
DataLoader.initialize_sample_data()

# Global game state
class WebGameState:
    def __init__(self):
        self.doctor = None
        self.current_patient = None
        self.score = 0
        self.patients = DataLoader.load_patients_from_json('data/sample_patients.json')
        if not self.patients:
            self.patients = DataLoader.get_sample_patients()
    
    def load_random_patient(self):
        if self.patients:
            self.current_patient = random.choice(self.patients)
            return True
        return False

game_state = WebGameState()

@app.route('/')
def main_menu():
    # Reset game state when returning to main menu
    if 'reset' in request.args:
        session.clear()
        game_state.doctor = None
        game_state.current_patient = None
    
    return render_template('main_menu.html')

@app.route('/specialization')
def specialization_select():
    specializations = get_available_specializations()
    return render_template('specialization_select.html', specializations=specializations)

@app.route('/select_specialization', methods=['POST'])
def select_specialization():
    specialization_name = request.form.get('specialization')
    
    # Find the selected specialization
    specializations = get_available_specializations()
    selected_spec = next((s for s in specializations if s.name == specialization_name), None)
    
    if selected_spec:
        # Create a doctor with the selected specialization
        game_state.doctor = Doctor(name="Dr. Player", specialization=selected_spec)
        
        # Load a random patient
        game_state.load_random_patient()
        
        return redirect(url_for('patient_view'))
    
    return redirect(url_for('specialization_select'))

@app.route('/patient')
def patient_view():
    if not game_state.doctor or not game_state.current_patient:
        return redirect(url_for('main_menu'))
    
    return render_template(
        'patient_view.html', 
        doctor=game_state.doctor, 
        patient=game_state.current_patient,
        tests=game_state.doctor.specialization.available_tests,
        treatments=game_state.doctor.specialization.available_treatments
    )

@app.route('/run_test', methods=['POST'])
def run_test():
    test_name = request.form.get('test')
    
    if game_state.current_patient and game_state.doctor.can_perform_test(test_name):
        result = game_state.current_patient.perform_test(test_name)
        return render_template(
            'test_result.html',
            test_name=test_name,
            result=result,
            patient=game_state.current_patient
        )
    
    return redirect(url_for('patient_view'))

@app.route('/apply_treatment', methods=['POST'])
def apply_treatment():
    treatment_name = request.form.get('treatment')
    
    if game_state.current_patient and game_state.doctor.can_perform_treatment(treatment_name):
        result = game_state.current_patient.apply_treatment(treatment_name)
        
        # Simulate treatment effect (improving patient condition)
        game_state.current_patient.update_condition(-1)  # Negative means improvement
        
        return render_template(
            'treatment_result.html',
            treatment_name=treatment_name,
            result=result,
            patient=game_state.current_patient
        )
    
    return redirect(url_for('patient_view'))

@app.route('/diagnose', methods=['POST'])
def diagnose():
    diagnosis = request.form.get('diagnosis')
    
    if game_state.current_patient:
        # For Phase 1, any diagnosis is considered correct
        # In Phase 2, we'll add logic to check if the diagnosis matches the patient's condition
        game_state.doctor.diagnose_patient(True)
        game_state.current_patient.diagnosis = diagnosis
        
        return render_template(
            'diagnosis_result.html',
            diagnosis=diagnosis,
            patient=game_state.current_patient,
            doctor=game_state.doctor
        )
    
    return redirect(url_for('patient_view'))

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)