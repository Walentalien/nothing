"""
VirtualDoctor - Web Demo Version
A medical simulation game with web interface to showcase Phase 3 features
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
import os
import random
import sys
import json
from datetime import datetime

# Create directories if they don't exist
os.makedirs('data/images', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Add import path
sys.path.append('.')

# Import our models
from models.patient import Patient, VitalSigns
from utils.image_generator import ImageGenerator
from models.doctor import Doctor, get_available_specializations
from models.diagnosis import diagnosis_catalog
from utils.game_state import GameState
from utils.db_manager import DBManager

app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Disable caching

# Initialize the database tables if needed
print("Database initialized with all tables")

# Initialize the game state
game_state = GameState()

# Initialize medical conditions in the database
DBManager.initialize_conditions()

# Set up a doctor and patient for demo purposes
specializations = get_available_specializations()
doctor = Doctor("Demo Doctor", specialization=specializations[0])
game_state.set_doctor(doctor)

# Either load from database or create a new patient
existing_patients = DBManager.get_all_patients()
if existing_patients:
    # Use the last patient from the database
    db_patient = existing_patients[-1]
    game_state.load_patient_from_db(db_patient.patient_id)
else:
    # Create a new random patient
    game_state.load_random_patient()
    # Save the patient to the database
    DBManager.save_patient(game_state.current_patient)

# Save doctor to database
DBManager.save_doctor(doctor)

# Create HTML templates
def create_templates():
    """Create the necessary HTML templates if they don't exist yet"""
    
    # Main layout template
    layout_html = """<!DOCTYPE html>
<html>
<head>
    <title>VirtualDoctor - Medical Simulation</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            min-height: 100vh;
        }
        header {
            background-color: #205493;
            color: white;
            padding: 15px 20px;
            margin-bottom: 20px;
        }
        h1 {
            margin: 0;
        }
        nav {
            background-color: #f0f0f0;
            padding: 10px 20px;
            margin-bottom: 20px;
        }
        nav a {
            color: #205493;
            margin-right: 15px;
            text-decoration: none;
            font-weight: bold;
        }
        nav a:hover {
            text-decoration: underline;
        }
        .card {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 20px;
            background-color: white;
        }
        .card-title {
            background-color: #f0f0f0;
            padding: 10px;
            margin: -15px -15px 15px -15px;
            border-bottom: 1px solid #ddd;
            font-weight: bold;
        }
        .vital-signs {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        .vital {
            padding: 5px;
            border-radius: 3px;
        }
        .vital-label {
            font-weight: bold;
            color: #666;
        }
        .vital-value {
            font-size: 1.1em;
        }
        .btn {
            display: inline-block;
            padding: 8px 16px;
            background-color: #205493;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            border: none;
            cursor: pointer;
            font-size: 14px;
            text-align: center;
        }
        .btn:hover {
            background-color: #112e51;
        }
        .btn-green {
            background-color: #2e8540;
        }
        .btn-green:hover {
            background-color: #1e5c2c;
        }
        .btn-orange {
            background-color: #ff7518;
        }
        .btn-orange:hover {
            background-color: #e56b10;
        }
        .btn-red {
            background-color: #cd2026;
        }
        .btn-red:hover {
            background-color: #981b1e;
        }
        .symptom-list {
            list-style-type: none;
            padding-left: 0;
        }
        .symptom-list li {
            padding: 5px 0;
        }
        .symptom-list li:before {
            content: "• ";
            color: #cd2026;
        }
        .test-list, .treatment-list, .diagnosis-list {
            list-style-type: none;
            padding-left: 0;
        }
        .test-list li, .treatment-list li, .diagnosis-list li {
            padding: 10px;
            border: 1px solid #ddd;
            margin-bottom: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .result-image {
            max-width: 100%;
            height: auto;
            margin: 10px 0;
        }
        .confidence-high {
            color: #2e8540;
        }
        .confidence-medium {
            color: #ff7518;
        }
        .confidence-low {
            color: #cd2026;
        }
        .normal {
            color: #2e8540;
        }
        .abnormal {
            color: #cd2026;
            font-weight: bold;
        }
        footer {
            margin-top: 50px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>VirtualDoctor - Medical Simulation</h1>
        </header>
        <nav>
            <a href="/">Home</a>
            <a href="/patient">Current Patient</a>
            <a href="/tests">Tests</a>
            <a href="/treatments">Treatments</a>
            <a href="/diagnose">Diagnose</a>
            <a href="/about">About</a>
        </nav>
        <main>
            {% block content %}{% endblock %}
        </main>
        <footer>
            <p>VirtualDoctor - Medical Simulation Game | Phase 3 Demo</p>
        </footer>
    </div>
</body>
</html>"""

    # Home page template
    home_html = """{% extends "layout.html" %}
{% block content %}
<div class="card">
    <div class="card-title">Welcome to VirtualDoctor</div>
    <p>VirtualDoctor is a medical simulation game designed to help students and healthcare professionals practice diagnostics and treatment skills.</p>
    <p>This web demo showcases the Phase 3 features including:</p>
    <ul>
        <li>Advanced medical imaging with ECGs and X-rays</li>
        <li>Detailed test results with dynamic generation</li>
        <li>Improved diagnosis matching based on test results</li>
        <li>Treatment effects with vital sign changes</li>
    </ul>
    <p><a href="/patient" class="btn btn-green">View Current Patient</a></p>
</div>
{% endblock %}"""

    # About page template
    about_html = """{% extends "layout.html" %}
{% block content %}
<div class="card">
    <div class="card-title">About VirtualDoctor</div>
    <p>VirtualDoctor is an educational medical simulation game designed to help medical students and healthcare professionals practice diagnostic and treatment skills in a risk-free virtual environment.</p>
    
    <h3>Features</h3>
    <ul>
        <li>Choose from multiple medical specializations</li>
        <li>Diagnose and treat virtual patients with realistic symptoms</li>
        <li>View medical imaging including ECGs and X-rays</li>
        <li>Analyze blood test results and other diagnostics</li>
        <li>Make diagnoses based on patient symptoms and test results</li>
        <li>Monitor your performance and accuracy</li>
    </ul>
    
    <h3>Phase 3 Enhancements</h3>
    <ul>
        <li>Advanced medical imaging with dynamically generated ECGs and X-rays</li>
        <li>Detailed database for patient records and medical history</li>
        <li>Enhanced test results with clinical recommendations</li>
        <li>Improved diagnosis matching using test results and symptoms</li>
    </ul>
    
    <p>This application was developed as an educational tool and should not replace actual medical training or professional medical advice.</p>
</div>
{% endblock %}"""

    # Patient view template
    patient_html = """{% extends "layout.html" %}
{% block content %}
<div class="card">
    <div class="card-title">Patient Information</div>
    <h2>{{ patient.name }}</h2>
    <p><strong>Age/Gender:</strong> {{ patient.age }} years, {{ patient.gender }}</p>
    <p><strong>Medical History:</strong> {{ patient.medical_history|join(', ') or 'None' }}</p>
    <p><strong>Condition:</strong> {{ condition_text }}</p>
    
    <h3>Vital Signs</h3>
    <div class="vital-signs">
        <div class="vital">
            <div class="vital-label">Heart Rate</div>
            <div class="vital-value">{{ patient.vital_signs.pulse }} BPM</div>
        </div>
        <div class="vital">
            <div class="vital-label">Blood Pressure</div>
            <div class="vital-value">{{ patient.vital_signs.systolic_bp }}/{{ patient.vital_signs.diastolic_bp }} mmHg</div>
        </div>
        <div class="vital">
            <div class="vital-label">Temperature</div>
            <div class="vital-value">{{ "%.1f"|format(patient.vital_signs.temperature) }}°C</div>
        </div>
        <div class="vital">
            <div class="vital-label">Respiratory Rate</div>
            <div class="vital-value">{{ patient.vital_signs.respiratory_rate }} breaths/min</div>
        </div>
        <div class="vital">
            <div class="vital-label">O₂ Saturation</div>
            <div class="vital-value">{{ patient.vital_signs.oxygen_saturation }}%</div>
        </div>
    </div>
    
    <h3>Current Symptoms</h3>
    {% if patient.current_symptoms %}
    <ul class="symptom-list">
        {% for symptom in patient.current_symptoms %}
        <li>{{ symptom }}</li>
        {% endfor %}
    </ul>
    {% else %}
    <p>No symptoms reported</p>
    {% endif %}
    
    <div style="margin-top: 20px;">
        <a href="/tests" class="btn">Run Tests</a>
        <a href="/treatments" class="btn btn-green">Administer Treatment</a>
        <a href="/diagnose" class="btn btn-orange">Make Diagnosis</a>
    </div>
</div>
{% endblock %}"""

    # Tests page template
    tests_html = """{% extends "layout.html" %}
{% block content %}
<div class="card">
    <div class="card-title">Available Tests</div>
    <p>Select a test to perform on the current patient:</p>
    
    <ul class="test-list">
        {% for test in tests %}
        <li>
            {{ test }}
            <a href="/run_test/{{ test|replace(' ', '_') }}" class="btn">Run Test</a>
        </li>
        {% endfor %}
    </ul>
    
    <div style="margin-top: 20px;">
        <a href="/patient" class="btn">Back to Patient</a>
    </div>
</div>
{% endblock %}"""

    # Test results template
    test_results_html = """{% extends "layout.html" %}
{% block content %}
<div class="card">
    <div class="card-title">Test Results: {{ test_name }}</div>
    <p>{{ result.message }}</p>
    
    <h3>Details</h3>
    {% if 'image_path' in result.details %}
    <div style="text-align: center;">
        <img src="/image/{{ result.details.image_path }}" alt="{{ test_name }}" class="result-image">
    </div>
    {% endif %}
    
    {% for key, value in result.details.items() %}
        {% if key != 'image_path' %}
        <div style="margin: 5px 0;">
            <strong>{{ key|replace('_', ' ')|capitalize }}:</strong> {{ value }}
        </div>
        {% endif %}
    {% endfor %}
    
    <h3>Interpretation</h3>
    <p>{{ result.interpretation }}</p>
    
    {% if result.is_abnormal %}
    <p class="abnormal">ABNORMAL FINDINGS DETECTED</p>
    {% else %}
    <p class="normal">Normal findings</p>
    {% endif %}
    
    {% if result.recommendations %}
    <h3>Recommendations</h3>
    <ul>
        {% for rec in result.recommendations %}
        <li>{{ rec }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    
    <div style="margin-top: 20px;">
        <a href="/tests" class="btn">Back to Tests</a>
        <a href="/patient" class="btn">Back to Patient</a>
    </div>
</div>
{% endblock %}"""

    # Treatments page template
    treatments_html = """{% extends "layout.html" %}
{% block content %}
<div class="card">
    <div class="card-title">Available Treatments</div>
    <p>Select a treatment to administer to the current patient:</p>
    
    <ul class="treatment-list">
        {% for treatment in treatments %}
        <li>
            {{ treatment }}
            <a href="/apply_treatment/{{ treatment|replace(' ', '_') }}" class="btn btn-green">Apply</a>
        </li>
        {% endfor %}
    </ul>
    
    <div style="margin-top: 20px;">
        <a href="/patient" class="btn">Back to Patient</a>
    </div>
</div>
{% endblock %}"""

    # Treatment results template
    treatment_results_html = """{% extends "layout.html" %}
{% block content %}
<div class="card">
    <div class="card-title">Treatment Applied: {{ treatment_name }}</div>
    <p>{{ result.message }}</p>
    
    {% if result.effects %}
    <h3>Effects</h3>
    <ul>
        {% for effect in result.effects %}
        <li>{{ effect }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    
    {% if result.vital_changes %}
    <h3>Vital Sign Changes</h3>
    <ul>
        {% for vital, change in result.vital_changes.items() %}
        <li><strong>{{ vital|replace('_', ' ')|capitalize }}:</strong> {{ change }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    
    <div style="margin-top: 20px;">
        <a href="/treatments" class="btn btn-green">Apply Another Treatment</a>
        <a href="/patient" class="btn">Back to Patient</a>
    </div>
</div>
{% endblock %}"""

    # Diagnosis page template
    diagnose_html = """{% extends "layout.html" %}
{% block content %}
<div class="card">
    <div class="card-title">Make Diagnosis</div>
    <p>Based on the patient's symptoms and test results, select the most likely diagnosis:</p>
    
    {% if diagnostic_matches %}
    <h3>Recommended Diagnoses</h3>
    <ul class="diagnosis-list">
        {% for diagnosis, confidence in diagnostic_matches %}
        <li>
            <div>
                <strong>{{ diagnosis.name }}</strong><br>
                <span class="
                    {% if confidence > 0.6 %}confidence-high
                    {% elif confidence > 0.3 %}confidence-medium
                    {% else %}confidence-low{% endif %}
                ">
                    Confidence: {{ (confidence * 100)|int }}%
                </span>
            </div>
            <a href="/make_diagnosis/{{ diagnosis.name|replace(' ', '_') }}/{{ (confidence * 100)|int }}" class="btn">Select</a>
        </li>
        {% endfor %}
    </ul>
    {% endif %}
    
    {% if other_diagnoses %}
    <h3>Other Possible Diagnoses</h3>
    <ul class="diagnosis-list">
        {% for diagnosis in other_diagnoses %}
        <li>
            <div>
                <strong>{{ diagnosis.name }}</strong>
            </div>
            <a href="/make_diagnosis/{{ diagnosis.name|replace(' ', '_') }}/0" class="btn">Select</a>
        </li>
        {% endfor %}
    </ul>
    {% endif %}
    
    <div style="margin-top: 20px;">
        <a href="/patient" class="btn">Back to Patient</a>
    </div>
</div>
{% endblock %}"""

    # Diagnosis results template
    diagnosis_results_html = """{% extends "layout.html" %}
{% block content %}
<div class="card">
    <div class="card-title">Diagnosis Made: {{ diagnosis.name }}</div>
    <p>{{ diagnosis.description }}</p>
    
    {% if is_correct %}
    <p class="normal">Your diagnosis appears to be accurate based on the patient's symptoms and test results.</p>
    {% else %}
    <p class="abnormal">Your diagnosis may not fully align with the patient's symptoms and test results.</p>
    {% endif %}
    
    <h3>Recommended Actions</h3>
    
    {% if diagnosis.recommended_tests %}
    <h4>Recommended Tests</h4>
    <ul>
        {% for test in diagnosis.recommended_tests %}
        <li>
            {% if test in performed_tests %}✓{% else %}□{% endif %} {{ test }}
        </li>
        {% endfor %}
    </ul>
    {% endif %}
    
    {% if diagnosis.recommended_treatments %}
    <h4>Recommended Treatments</h4>
    <ul>
        {% for treatment in diagnosis.recommended_treatments %}
        <li>{{ treatment }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    
    {% if doctor %}
    <p><strong>Current score:</strong> {{ doctor.score }}</p>
    {% endif %}
    
    <div style="margin-top: 20px;">
        <a href="/patient" class="btn">Back to Patient</a>
        <a href="/next_patient" class="btn btn-green">Next Patient</a>
    </div>
</div>
{% endblock %}"""

    # Write templates to files
    with open('templates/layout.html', 'w') as f:
        f.write(layout_html)
    
    with open('templates/home.html', 'w') as f:
        f.write(home_html)
    
    with open('templates/about.html', 'w') as f:
        f.write(about_html)
    
    with open('templates/patient.html', 'w') as f:
        f.write(patient_html)
    
    with open('templates/tests.html', 'w') as f:
        f.write(tests_html)
    
    with open('templates/test_results.html', 'w') as f:
        f.write(test_results_html)
    
    with open('templates/treatments.html', 'w') as f:
        f.write(treatments_html)
    
    with open('templates/treatment_results.html', 'w') as f:
        f.write(treatment_results_html)
    
    with open('templates/diagnose.html', 'w') as f:
        f.write(diagnose_html)
    
    with open('templates/diagnosis_results.html', 'w') as f:
        f.write(diagnosis_results_html)

# Create templates before the app starts
create_templates()

# Helper functions
def get_condition_text(severity):
    if severity <= 3:
        return "Mild"
    elif severity <= 6:
        return "Moderate"
    elif severity <= 8:
        return "Serious"
    else:
        return "Critical"

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/patient')
def patient():
    if not game_state.current_patient:
        game_state.load_random_patient()
    
    return render_template(
        'patient.html',
        patient=game_state.current_patient,
        condition_text=get_condition_text(game_state.current_patient.condition_severity)
    )

@app.route('/tests')
def tests():
    if not game_state.doctor or not game_state.doctor.specialization:
        return redirect(url_for('home'))
    
    return render_template(
        'tests.html',
        tests=game_state.doctor.specialization.available_tests
    )

@app.route('/run_test/<test_name>')
def run_test(test_name):
    test_name = test_name.replace('_', ' ')
    
    if not game_state.current_patient:
        return redirect(url_for('patient'))
    
    # Run the test
    result = game_state.current_patient.perform_test(test_name)
    
    # Save the result in the game state
    game_state.save_test_result(test_name, result)
    
    # Save test result to PostgreSQL database
    if test_name and result:
        # Serialize the result properly
        result_data = {
            'values': result,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save to database
        DBManager.save_test_result(
            game_state.current_patient.patient_id,
            test_name,
            result_data
        )
        
        # If this is an imaging test, save the image record too
        if test_name in ['X-ray', 'ECG', 'MRI']:
            # Generate a filename for the image
            image_path = f"data/images/{test_name.lower()}_{game_state.current_patient.patient_id}.png"
            
            # Save image metadata to database
            DBManager.save_imaging_result(
                game_state.current_patient.patient_id,
                test_name,
                image_path,
                f"Results from {test_name} test"
            )
    
    return render_template(
        'test_results.html',
        test_name=test_name,
        result=result
    )

@app.route('/image/<path:image_path>')
def get_image(image_path):
    return send_file(image_path)

@app.route('/treatments')
def treatments():
    if not game_state.doctor or not game_state.doctor.specialization:
        return redirect(url_for('home'))
    
    return render_template(
        'treatments.html',
        treatments=game_state.doctor.specialization.available_treatments
    )

@app.route('/apply_treatment/<treatment_name>')
def apply_treatment(treatment_name):
    treatment_name = treatment_name.replace('_', ' ')
    
    if not game_state.current_patient:
        return redirect(url_for('patient'))
    
    # Apply the treatment
    result = game_state.current_patient.apply_treatment(treatment_name)
    
    # Save treatment to the PostgreSQL database
    if treatment_name and result:
        # Format vital signs changes
        vital_changes = {}
        if hasattr(result, 'vital_changes') and result.vital_changes:
            vital_changes = result.vital_changes
        
        # Format the treatment record data
        treatment_data = {
            'effects': str(result),
            'vital_changes': json.dumps(vital_changes),
            'treatment_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Save to database
        DBManager.save_treatment_record(
            game_state.current_patient.patient_id,
            treatment_name,
            treatment_data
        )
        
        # Also update the patient record in the database
        DBManager.save_patient(game_state.current_patient)
    
    return render_template(
        'treatment_results.html',
        treatment_name=treatment_name,
        result=result
    )

@app.route('/diagnose')
def diagnose():
    if not game_state.current_patient:
        return redirect(url_for('patient'))
    
    patient = game_state.current_patient
    
    # Get test names from tests performed
    performed_tests = [test['test'] for test in patient.tests_performed]
    
    # Get diagnostic matches based on symptoms and tests
    diagnostic_matches = diagnosis_catalog.match_diagnosis(
        symptoms=patient.current_symptoms,
        tests_performed=performed_tests
    )
    
    # Get all diagnoses for display
    all_diagnoses = diagnosis_catalog.get_all_diagnoses()
    
    # Sort diagnoses by confidence
    matched_names = [d[0].name for d in diagnostic_matches]
    other_diagnoses = [d for d in all_diagnoses if d.name not in matched_names]
    other_diagnoses.sort(key=lambda x: x.name)
    
    return render_template(
        'diagnose.html',
        diagnostic_matches=diagnostic_matches,
        other_diagnoses=other_diagnoses
    )

@app.route('/make_diagnosis/<diagnosis_name>/<confidence>')
def make_diagnosis(diagnosis_name, confidence):
    diagnosis_name = diagnosis_name.replace('_', ' ')
    confidence = int(confidence) / 100.0
    
    if not game_state.current_patient:
        return redirect(url_for('patient'))
    
    # Get the diagnosis
    diagnosis = diagnosis_catalog.get_diagnosis(diagnosis_name)
    if not diagnosis:
        return redirect(url_for('diagnose'))
        
    # Save the diagnosis to the database
    # Set patient's diagnosis
    game_state.current_patient.diagnosis = diagnosis_name
    
    # Check if it's correct (simplified for demo - in real app would check against true diagnosis)
    is_correct = confidence > 0.7  # Assume diagnosis is correct if confidence is high
    
    # Save patient data to PostgreSQL database with updated diagnosis
    DBManager.save_patient(game_state.current_patient)
    
    # Record the diagnosis in the database
    diagnosis_result = {
        'diagnosis_name': diagnosis_name,
        'is_correct': is_correct,
        'confidence': confidence * 100,  # Convert to percentage
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save the diagnosis result as a special type of test result
    DBManager.save_test_result(
        game_state.current_patient.patient_id, 
        "Final_Diagnosis", 
        diagnosis_result
    )
    
    # Check if diagnosis is correct
    is_correct = confidence > 0.6
    if confidence == 0 and len(game_state.current_patient.current_symptoms) == 0:
        # If no symptoms and chose "No significant findings", that's correct
        if diagnosis.name == "No Significant Findings":
            is_correct = True
    
    # Update doctor's statistics
    if game_state.doctor:
        game_state.doctor.diagnose_patient(is_correct)
    
    # Set the diagnosis on the patient
    game_state.current_patient.diagnosis = diagnosis.name
    
    # Update patient condition
    if is_correct:
        # Improve patient condition due to correct diagnosis
        game_state.current_patient.update_condition(-2)
    else:
        # Worsen patient condition slightly due to incorrect diagnosis
        game_state.current_patient.update_condition(1)
    
    # Get performed tests for display
    performed_tests = []
    if game_state.current_patient:
        performed_tests = [test['test'] for test in game_state.current_patient.tests_performed]
    
    return render_template(
        'diagnosis_results.html',
        diagnosis=diagnosis,
        is_correct=is_correct,
        performed_tests=performed_tests,
        doctor=game_state.doctor
    )

@app.route('/next_patient')
def next_patient():
    # Complete current case
    if game_state.current_patient:
        game_state.complete_current_case()
    
    # Load a new patient
    game_state.load_random_patient()
    
    return redirect(url_for('patient'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)