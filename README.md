# VirtualDoctor Project Setup Guide


## Setup Instructions
Git command that helped me :
`git config --global credential.helper store`
So git stores your credentialss
### Requirements
- Python 3.11 or higher
- PostgreSQL database (or SQLite)

### Python Dependencies
Install required dependencies:

```bash
pip install kivy matplotlib numpy psycopg2-binary sqlalchemy
```

### Database Setup
Create a `.env` file in the project root with your database connection:

```
DATABASE_URL=sqlite:///virtualdoctor.db
```

### Running the Applications

Console version:
```bash
python main.py
```

Web interface:
```bash
python web_doctor.py
```

Kivy GUI:
```bash
python kivy_doctor.py
```

## Note About Game Progress
Your progress will be saved in the database specified by DATABASE_URL.

# VirtualDoctor - Medical Simulation Game

## Overview

VirtualDoctor is an immersive educational medical simulation game that provides realistic patient diagnosis and treatment scenarios for medical training and education. The application supports multiple interfaces including a cross-platform Kivy GUI, web interface, and console version.


## Current Features

### 1. User Authentication System

**Implementation**: Secure user registration and login with database persistence.

```python
# User authentication in screens/login_screen.py
def login(self, instance):
    username = self.username_input.text.strip()
    password = self.password_input.text.strip()
    
    user = DBManager.authenticate_user(username, password)
    if user:
        app = App.get_running_app()
        app.current_user = user
        self.manager.current = 'dashboard'
```

**Features**:
- Secure password hashing with werkzeug
- User session management
- Dashboard with user statistics
- Progress tracking across sessions

### 2. Medical Specialization System

**Implementation**: Dynamic specialization selection with specialized medical knowledge.

```python
# Specialization selection in kivy_doctor.py
def select_specialization(self, instance):
    selected_spec = instance.specialization
    app = App.get_running_app()
    app.game_state.set_doctor_specialization(selected_spec.name)
    
    # Load first patient for this specialization
    if app.game_state.load_random_patient():
        self.manager.get_screen('patient').update_patient_data()
        self.manager.current = 'patient'
```

**Available Specializations**:
- Cardiology - Heart and cardiovascular system
- Neurology - Nervous system disorders
- Pediatrics - Children's medicine
- Emergency Medicine - Critical care
- Internal Medicine - General adult medicine

### 3. Patient Simulation Engine

**Implementation**: Realistic patient models with dynamic vital signs and symptoms.

```python
# Patient model in models/patient.py
class Patient:
    def __init__(self, patient_id, name, age, gender, medical_history, 
                 current_symptoms, vital_signs, diagnosis=None, condition_severity=3):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.vital_signs = vital_signs
        self.condition_severity = condition_severity
        self.tests_performed = []
```

**Patient Features**:
- Dynamic vital signs (heart rate, blood pressure, temperature, respiratory rate, oxygen saturation)
- Medical history tracking
- Symptom presentation
- Condition severity levels (1-10)
- Test results storage

### 4. Medical Testing System

**Implementation**: Comprehensive diagnostic testing with realistic results.

```python
# Test execution in kivy_doctor.py
def run_test(self, instance):
    test_name = instance.test_name
    app = App.get_running_app()
    patient = app.game_state.current_patient
    
    if patient:
        results = patient.run_test(test_name)
        app.game_state.save_test_result(test_name, results)
        
        # Navigate to results screen
        self.manager.get_screen('test_results').set_test_results(test_name, results)
        self.manager.current = 'test_results'
```

**Available Tests**:
- Blood Tests (CBC, Chemistry Panel, Cardiac Markers)
- Imaging (X-Ray, CT, MRI, Ultrasound)
- Cardiac (ECG, Echocardiogram, Stress Test)
- Neurological (EEG, Lumbar Puncture, Reflex Tests)
- Respiratory (Pulmonary Function, Arterial Blood Gas)

### 5. Medical Imaging Generation

**Implementation**: Procedural generation of medical images based on patient conditions.

```python
# Image generation in utils/image_generator.py
class ImageGenerator:
    @staticmethod
    def generate_ecg(patient, abnormalities=None):
        """Generate ECG waveform based on patient condition"""
        # Create realistic ECG patterns
        time = np.linspace(0, 3, 1500)  # 3 seconds
        ecg_signal = ImageGenerator._generate_ecg_waveform(time, patient.pulse)
        
        # Apply abnormalities based on patient condition
        if abnormalities:
            ecg_signal = ImageGenerator._apply_ecg_abnormalities(ecg_signal, abnormalities)
```

**Imaging Features**:
- Dynamic ECG generation based on heart rate and conditions
- Chest X-ray simulation with pathology indicators
- Customizable abnormality patterns
- Image saving and retrieval system

### 6. Treatment Application System

**Implementation**: Medical treatment administration with patient response simulation.

```python
# Treatment application in utils/game_state.py
def apply_treatment(self, treatment_name: str) -> Dict:
    available_treatments = self.doctor.specialization.treatments
    treatment = next((t for t in available_treatments if t.name == treatment_name), None)
    
    if treatment:
        results = self.current_patient.apply_treatment(treatment)
        DBManager.save_treatment_record(
            self.current_patient.patient_id,
            treatment_name,
            results.get("effects", {}),
            results.get("vital_changes", {})
        )
        return results
```

**Treatment Features**:
- Specialization-specific treatment options
- Patient response simulation
- Vital sign changes tracking
- Treatment history logging

### 7. Medication Management System

**Implementation**: Comprehensive medication database with administration tracking.

```python
# Medication administration in utils/medication_manager.py
class MedicationManager:
    @staticmethod
    def administer_medication(patient, medication_name, dosage, route):
        medication = MedicationManager.get_medication_by_name(medication_name)
        if medication:
            response = LocalMedication.simulate_patient_response(
                patient, medication, dosage, route
            )
            # Save administration record
            record = LocalMedicationRecord(
                patient_id=patient.patient_id,
                medication_id=medication['id'],
                dosage=dosage,
                administration_route=route,
                effectiveness=response['effectiveness']
            )
```

**Medication Features**:
- Extensive medication database (antibiotics, painkillers, cardiac drugs)
- Dosage and administration route tracking
- Patient response simulation
- Side effects and interactions monitoring
- Effectiveness scoring

### 8. Diagnostic System

**Implementation**: Medical diagnosis with confidence scoring and feedback.

```python
# Diagnosis system in kivy_doctor.py
def make_diagnosis(self, instance):
    diagnosis = instance.diagnosis
    confidence = instance.confidence
    app = App.get_running_app()
    patient = app.game_state.current_patient
    
    if patient and patient.diagnosis:
        is_correct = (diagnosis.lower() == patient.diagnosis.lower())
        score = confidence if is_correct else max(0, 100 - confidence)
        
        app.game_state.add_score(score)
        
        # Show results
        self.manager.get_screen('diagnosis_results').set_diagnosis_results(
            diagnosis, is_correct
        )
```

**Diagnostic Features**:
- Confidence-based scoring system
- Immediate feedback on accuracy
- Score tracking and performance metrics
- Differential diagnosis support

### 9. Game State Management

**Implementation**: Comprehensive game progression and statistics tracking.

```python
# Game state in utils/game_state.py
class GameState:
    def __init__(self):
        self.doctor = None
        self.current_patient = None
        self.score = 0
        self.game_difficulty = 'medium'
        self.current_level = 1
        self.cases_completed = []
        self.session_start_time = datetime.now()
```

**State Features**:
- Multi-level progression system
- Difficulty adjustment (easy, medium, hard)
- Session statistics tracking
- Patient case completion logging
- Performance analytics

## User Interface Design

### Screen Architecture

The Kivy GUI implements a screen management system with dedicated screens for each game component:

```python
# Screen manager setup in kivy_doctor.py
def build(self):
    sm = ScreenManager()
    
    # Core game screens
    sm.add_widget(MainMenuScreen(name='main_menu'))
    sm.add_widget(SpecializationScreen(name='specialization'))
    sm.add_widget(PatientScreen(name='patient'))
    sm.add_widget(TestsScreen(name='tests'))
    sm.add_widget(TreatmentsScreen(name='treatments'))
    sm.add_widget(DiagnosisScreen(name='diagnosis'))
    sm.add_widget(MedicationsScreen(name='medications'))
    
    # User management screens
    sm.add_widget(LoginScreen(name='login'))
    sm.add_widget(DashboardScreen(name='dashboard'))
    
    return sm
```

### Visual Design Elements

- **Color Scheme**: Medical blue theme with high contrast text
- **Layout**: Responsive grid and box layouts
- **Navigation**: Intuitive button-based navigation between screens
- **Data Display**: Organized vital signs panels and test results

## Data Storage

### PostgreSQL Production Database

```python
# Database models in models/database_models.py
class Patient(Base):
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    vital_signs = Column(Text)  # JSON serialized object
    test_results = relationship("TestResult", back_populates="patient")
    treatment_records = relationship("TreatmentRecord", back_populates="patient")
```

### SQLite Local Development

```python
# Local database in utils/local_db.py
def init_db():
    """Initialize local SQLite database"""
    Base.metadata.create_all(engine)
    
    # Initialize sample data if needed
    session = Session()
    if session.query(LocalMedication).count() == 0:
        initialize_sample_medications(session)
    session.close()
```

## Planned Features

### Phase 4: Advanced Medical Simulation

#### 1. Advanced Pathophysiology Simulation
- **Multi-system Disease Modeling**: Complex conditions affecting multiple organ systems
- **Disease Progression**: Time-based condition evolution
- **Complication Modeling**: Realistic adverse event simulation

#### 2. Enhanced Medical Imaging
- **3D Visualization**: Interactive 3D medical models
- **DICOM Support**: Real medical imaging format compatibility
- **AI-Assisted Reading**: Automated finding detection with educational overlay

#### 3. Procedural Simulation
- **Virtual Procedures**: Step-by-step medical procedure training
- **Haptic Feedback**: Touch-based simulation for supported devices
- **Skill Assessment**: Procedure technique evaluation

#### 4. Advanced Pharmacology
- **Drug Interactions**: Complex medication interaction modeling
- **Pharmacokinetics**: Drug absorption, distribution, metabolism simulation
- **Personalized Medicine**: Patient-specific drug response modeling

#### 5. Collaborative Features
- **Multi-User Cases**: Team-based medical scenarios
- **Peer Review**: Case discussion and consultation system
- **Instructor Dashboard**: Educational oversight and assessment tools

#### 6. Assessment and Certification
- **Competency Testing**: Standardized medical knowledge assessment
- **Skill Certification**: Procedure and diagnostic skill validation
- **Progress Analytics**: Detailed learning outcome tracking

#### 7. Real-World Integration
- **Medical Record Import**: Practice with anonymized real cases
- **Hospital Workflow**: Healthcare system process simulation
- **Continuing Education**: CME credit integration

#### 8. Mobile Optimization
- **Touch Interface**: Optimized mobile interaction design
- **Offline Mode**: Downloadable cases for offline study
- **Cross-Platform Sync**: Progress synchronization across devices

### Technical Enhancements

#### 1. Performance Optimization
- **Caching System**: Intelligent data caching for improved performance
- **Background Processing**: Asynchronous task handling
- **Memory Management**: Optimized resource usage

#### 2. Accessibility Features
- **Screen Reader Support**: Full accessibility compliance
- **Keyboard Navigation**: Complete keyboard-only operation
- **Visual Accommodations**: High contrast and text scaling options

#### 3. Localization
- **Multi-Language Support**: International medical terminology
- **Regional Adaptations**: Location-specific medical practices
- **Cultural Sensitivity**: Diverse patient representation

## Installation and Setup

### Requirements
```bash
# Core dependencies
pip install kivy sqlalchemy psycopg2-binary
pip install matplotlib numpy scipy werkzeug

# Development dependencies
pip install pytest 
```

### Database Setup

#### PostgreSQL (Production)
```bash
# Set environment variables
export DATABASE_URL="postgresql://user:password@localhost/virtualdoctor"
export PGPORT=5432
export PGUSER=postgres
```

#### SQLite (Local Development)
```python
# Automatic initialization
from utils.local_db import init_db
init_db()  # Creates local database with sample data
```

### Running the Application

#### Kivy GUI Version
```bash
python kivy_doctor.py      # PostgreSQL version
python kivy_local.py       # SQLite version # Wasn't working properlys
```


## Development Guidelines

### Code Organization
- **Models**: Patient, medication, and medical condition definitions
- **Screens**: Kivy UI screen implementations
- **Utils**: Database managers, game state, and helper functions
- **Data**: Sample patient data and medical imaging assets

### Testing
```python
# Run test suite
python test_local_sqlite.py    # Test SQLite implementation
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request with detailed description

## Educational Value

VirtualDoctor provides hands-on medical training through:
- **Realistic Patient Scenarios**: Based on actual medical cases
- **Evidence-Based Medicine**: Treatments and diagnostics follow medical guidelines
- **Progressive Learning**: Difficulty scaling with user competency
- **Immediate Feedback**: Real-time assessment and guidance
- **Comprehensive Coverage**: Multiple medical specialties and conditions

The simulation environment allows medical students and professionals to practice clinical decision-making in a safe, controlled setting while developing critical diagnostic and treatment skills.