import random
from datetime import datetime
from typing import List, Dict, Optional

class VitalSigns:
    """
    Represents patient vital signs like pulse, blood pressure, temperature, etc.
    """
    def __init__(self, 
                 pulse: int = 80, 
                 systolic_bp: int = 120, 
                 diastolic_bp: int = 80,
                 temperature: float = 36.6,
                 respiratory_rate: int = 16,
                 oxygen_saturation: int = 98):
        """
        Initialize vital signs with normal values by default.
        
        Args:
            pulse: Heart rate in beats per minute
            systolic_bp: Systolic blood pressure in mmHg
            diastolic_bp: Diastolic blood pressure in mmHg
            temperature: Body temperature in Celsius
            respiratory_rate: Breaths per minute
            oxygen_saturation: Oxygen saturation percentage (SpO2)
        """
        self.pulse = pulse
        self.systolic_bp = systolic_bp
        self.diastolic_bp = diastolic_bp
        self.temperature = temperature
        self.respiratory_rate = respiratory_rate
        self.oxygen_saturation = oxygen_saturation
    
    def get_formatted_bp(self) -> str:
        """Return blood pressure in standard format."""
        return f"{self.systolic_bp}/{self.diastolic_bp} mmHg"
    
    def get_vitals_dict(self) -> Dict:
        """Return all vital signs as a dictionary."""
        return {
            'pulse': self.pulse,
            'blood_pressure': self.get_formatted_bp(),
            'temperature': f"{self.temperature:.1f}°C",
            'respiratory_rate': self.respiratory_rate,
            'oxygen_saturation': f"{self.oxygen_saturation}%"
        }
    
    def update_vitals(self, **kwargs) -> None:
        """
        Update vital signs with new values.
        
        Args:
            **kwargs: Vital signs to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Patient:
    """
    Represents a patient in the medical simulation with personal info, 
    medical history, symptoms, vital signs, and current condition.
    """
    def __init__(self, 
                 patient_id: str,
                 name: str,
                 age: int,
                 gender: str,
                 medical_history: List[str] = None,
                 current_symptoms: List[str] = None,
                 vital_signs: VitalSigns = None,
                 diagnosis: str = None,
                 condition_severity: int = 1):  # 1-10 scale, 10 being most severe
        """
        Initialize a patient with their basic information.
        
        Args:
            patient_id: Unique identifier for the patient
            name: Patient name
            age: Patient age in years
            gender: Patient gender
            medical_history: List of past medical conditions
            current_symptoms: List of current symptoms
            vital_signs: Patient's vital signs
            diagnosis: Current diagnosis if any
            condition_severity: Severity of condition (1-10)
        """
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.medical_history = medical_history or []
        self.current_symptoms = current_symptoms or []
        self.vital_signs = vital_signs or VitalSigns()
        self.diagnosis = diagnosis
        self.condition_severity = condition_severity
        self.admission_time = datetime.now()
        self.treatments_applied = []
        self.tests_performed = []
    
    def add_symptom(self, symptom: str) -> None:
        """Add a new symptom to the patient."""
        if symptom not in self.current_symptoms:
            self.current_symptoms.append(symptom)
    
    def remove_symptom(self, symptom: str) -> None:
        """Remove a symptom from the patient."""
        if symptom in self.current_symptoms:
            self.current_symptoms.remove(symptom)
    
    def get_patient_info(self) -> Dict:
        """Return basic patient information as a dictionary."""
        return {
            'id': self.patient_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'medical_history': self.medical_history,
            'admission_time': self.admission_time.strftime("%Y-%m-%d %H:%M")
        }
    
    def apply_treatment(self, treatment: str) -> Dict:
        """
        Apply a treatment to the patient and record its effects.
        
        Args:
            treatment: Name of the treatment applied
            
        Returns:
            Dict with treatment results
        """
        self.treatments_applied.append({
            'treatment': treatment,
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Phase 2: Implement treatment effects
        result = {
            'success': True,
            'message': f"Treatment '{treatment}' applied.",
            'effects': [],
            'severity_change': 0,
            'vital_changes': {}
        }
        
        # Define medication effects
        if treatment == "Pain Relief":
            # Pain relievers
            if any(s in self.current_symptoms for s in ["Headache", "Pain", "Chest Pain", "Abdominal Pain"]):
                result['effects'].append("Pain reduced")
                self.current_symptoms = [s for s in self.current_symptoms if s not in ["Headache", "Pain"]]
                
                if "Chest Pain" in self.current_symptoms:
                    result['effects'].append("Chest pain partially relieved but not eliminated")
                
                result['severity_change'] = -1
                
        elif treatment == "Antibiotics":
            # Simulate antibiotic effects based on condition
            if any(s in self.current_symptoms for s in ["Fever", "Cough"]):
                # Simulate gradual improvement
                if random.random() < 0.7:  # 70% chance of improvement
                    result['effects'].append("Antibiotic appears to be effective")
                    result['severity_change'] = -2
                    
                    # Temperature reduction
                    if self.vital_signs.temperature > 37.5:
                        new_temp = max(36.8, self.vital_signs.temperature - random.uniform(0.5, 1.2))
                        self.vital_signs.temperature = new_temp
                        result['vital_changes']['temperature'] = f"Decreased to {new_temp:.1f}°C"
                else:
                    result['effects'].append("Patient's response to antibiotics is still developing")
                    result['severity_change'] = -1
            else:
                result['effects'].append("No immediate effect observed")
                
        elif treatment == "Beta-blockers":
            # Primarily affects heart rate and blood pressure
            if self.vital_signs.pulse > 90:
                new_pulse = max(70, self.vital_signs.pulse - random.randint(10, 25))
                self.vital_signs.pulse = new_pulse
                result['vital_changes']['heart_rate'] = f"Decreased to {new_pulse} BPM"
                result['effects'].append("Heart rate decreased")
            
            if self.vital_signs.systolic_bp > 140 or self.vital_signs.diastolic_bp > 90:
                new_systolic = max(120, self.vital_signs.systolic_bp - random.randint(15, 30))
                new_diastolic = max(80, self.vital_signs.diastolic_bp - random.randint(5, 15))
                self.vital_signs.systolic_bp = new_systolic
                self.vital_signs.diastolic_bp = new_diastolic
                result['vital_changes']['blood_pressure'] = f"Decreased to {new_systolic}/{new_diastolic} mmHg"
                result['effects'].append("Blood pressure reduced")
                
            if 'Chest Pain' in self.current_symptoms:
                if random.random() < 0.6:  # 60% chance of improvement
                    self.current_symptoms.remove('Chest Pain')
                    result['effects'].append("Chest pain relieved")
                else:
                    result['effects'].append("Chest pain partially improved")
                    
            result['severity_change'] = -2 if result['effects'] else -1
                
        elif treatment == "ACE Inhibitors":
            # Blood pressure medication
            if self.vital_signs.systolic_bp > 130 or self.vital_signs.diastolic_bp > 85:
                new_systolic = max(120, self.vital_signs.systolic_bp - random.randint(10, 20))
                new_diastolic = max(80, self.vital_signs.diastolic_bp - random.randint(5, 10))
                self.vital_signs.systolic_bp = new_systolic
                self.vital_signs.diastolic_bp = new_diastolic
                result['vital_changes']['blood_pressure'] = f"Decreased to {new_systolic}/{new_diastolic} mmHg"
                result['effects'].append("Blood pressure reduced")
                result['severity_change'] = -1
            else:
                # If BP is already normal or low, could cause hypotension
                new_systolic = max(90, self.vital_signs.systolic_bp - random.randint(5, 15))
                new_diastolic = max(60, self.vital_signs.diastolic_bp - random.randint(3, 8))
                self.vital_signs.systolic_bp = new_systolic
                self.vital_signs.diastolic_bp = new_diastolic
                
                if new_systolic < 100:
                    result['vital_changes']['blood_pressure'] = f"Decreased to {new_systolic}/{new_diastolic} mmHg"
                    result['effects'].append("Blood pressure dropped too low - possible hypotension")
                    if 'Dizziness' not in self.current_symptoms:
                        self.current_symptoms.append('Dizziness')
                        result['effects'].append("Patient developed dizziness")
                    result['severity_change'] = 1  # Worsen condition due to side effect
                
        elif treatment == "Oxygen Therapy":
            # Improve oxygen saturation
            if self.vital_signs.oxygen_saturation < 95:
                new_o2 = min(99, self.vital_signs.oxygen_saturation + random.randint(3, 8))
                self.vital_signs.oxygen_saturation = new_o2
                result['vital_changes']['oxygen_saturation'] = f"Increased to {new_o2}%"
                result['effects'].append("Oxygen saturation improved")
                
                if 'Shortness of Breath' in self.current_symptoms:
                    if random.random() < 0.7:  # 70% chance of improvement
                        self.current_symptoms.remove('Shortness of Breath')
                        result['effects'].append("Breathing difficulty relieved")
                    else:
                        result['effects'].append("Breathing difficulty partially improved")
                        
                result['severity_change'] = -2
            else:
                result['effects'].append("Oxygen levels already adequate")
                
        elif treatment == "IV Fluids":
            # Improve blood pressure if low, help with dehydration
            if self.vital_signs.systolic_bp < 100:
                new_systolic = min(120, self.vital_signs.systolic_bp + random.randint(10, 20))
                new_diastolic = min(80, self.vital_signs.diastolic_bp + random.randint(5, 10))
                self.vital_signs.systolic_bp = new_systolic
                self.vital_signs.diastolic_bp = new_diastolic
                result['vital_changes']['blood_pressure'] = f"Increased to {new_systolic}/{new_diastolic} mmHg"
                result['effects'].append("Blood pressure stabilized")
                
            # Simulate hydration effects
            if 'Dizziness' in self.current_symptoms:
                if random.random() < 0.8:  # 80% chance of improvement
                    self.current_symptoms.remove('Dizziness')
                    result['effects'].append("Dizziness relieved")
            
            result['severity_change'] = -1
                
        elif treatment == "Defibrillation":
            # Used in cardiac emergencies
            if self.condition_severity >= 8 and 'Chest Pain' in self.current_symptoms:
                if random.random() < 0.7:  # 70% success rate
                    result['effects'].append("Cardiac rhythm restored")
                    
                    new_pulse = random.randint(70, 90)
                    self.vital_signs.pulse = new_pulse
                    result['vital_changes']['heart_rate'] = f"Stabilized at {new_pulse} BPM"
                    
                    result['severity_change'] = -3
                else:
                    result['effects'].append("Defibrillation performed, patient requires continued care")
                    result['severity_change'] = -1
            else:
                result['effects'].append("Defibrillation not indicated for current condition")
                result['severity_change'] = 0
                
        elif treatment == "Intubation":
            # Emergency airway management
            if self.vital_signs.oxygen_saturation < 85 or 'Shortness of Breath' in self.current_symptoms and self.condition_severity >= 7:
                result['effects'].append("Airway secured, ventilation established")
                
                new_o2 = min(98, self.vital_signs.oxygen_saturation + random.randint(10, 15))
                self.vital_signs.oxygen_saturation = new_o2
                result['vital_changes']['oxygen_saturation'] = f"Increased to {new_o2}%"
                
                new_resp = 14  # Controlled by ventilator
                self.vital_signs.respiratory_rate = new_resp
                result['vital_changes']['respiratory_rate'] = f"Controlled at {new_resp} breaths/min"
                
                result['severity_change'] = -3
            else:
                result['effects'].append("Intubation not indicated for current condition")
                result['severity_change'] = 0
        
        else:
            # Generic treatment effect
            symptom_improvement = random.random() < 0.6  # 60% chance of symptom improvement
            
            if symptom_improvement and self.current_symptoms:
                symptom_to_remove = random.choice(self.current_symptoms)
                self.current_symptoms.remove(symptom_to_remove)
                result['effects'].append(f"{symptom_to_remove} relieved")
                
            result['severity_change'] = -1 if symptom_improvement else 0
        
        # Apply the overall severity change
        if result['severity_change'] != 0:
            self.update_condition(result['severity_change'])
            
            if result['severity_change'] < 0:
                result['message'] = f"Treatment '{treatment}' applied successfully. Patient's condition is improving."
            elif result['severity_change'] > 0:
                result['message'] = f"Treatment '{treatment}' applied, but patient condition has worsened."
        
        return result
    
    def perform_test(self, test_name: str) -> Dict:
        """
        Perform a medical test on the patient.
        
        Args:
            test_name: Name of the test to perform
            
        Returns:
            Dict with test results
        """
        from datetime import datetime
        import random
        
        # Try to import the image generator for Phase 3 features
        try:
            from utils.image_generator import ImageGenerator
            has_image_generator = True
        except ImportError:
            has_image_generator = False
        
        # Add to performed tests
        self.tests_performed.append({
            'test': test_name,
            'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Phase 3: Generate detailed test results with imaging when applicable
        result = {
            'success': True,
            'message': f"Test '{test_name}' performed successfully.",
            'details': {},
            'interpretation': "Normal findings",
            'is_abnormal': False,
            'recommendations': []
        }
        
        # Determine if the result should be abnormal based on symptoms and condition severity
        abnormal_chance = 0.2  # Base chance
        if self.current_symptoms:
            # Higher chance of abnormal result if patient has symptoms
            abnormal_chance += min(0.6, len(self.current_symptoms) * 0.1)
        
        # Higher chance of abnormal result if condition is severe
        abnormal_chance += min(0.2, self.condition_severity * 0.02)
        
        is_abnormal = random.random() < abnormal_chance
        result['is_abnormal'] = is_abnormal
        
        # Generate test-specific results
        if test_name == "Blood Pressure":
            # Get stored values or generate new ones
            systolic = self.vital_signs.systolic_bp
            diastolic = self.vital_signs.diastolic_bp
            
            # Classification
            bp_category = "Normal"
            if systolic >= 180 or diastolic >= 120:
                bp_category = "Hypertensive Crisis"
            elif systolic >= 140 or diastolic >= 90:
                bp_category = "Stage 2 Hypertension"
            elif systolic >= 130 or diastolic >= 80:
                bp_category = "Stage 1 Hypertension"
            elif systolic >= 120 and systolic < 130 and diastolic < 80:
                bp_category = "Elevated"
                
            result['details'] = {
                'systolic': systolic,
                'diastolic': diastolic,
                'category': bp_category
            }
            
            if bp_category != "Normal":
                result['is_abnormal'] = True
                result['interpretation'] = f"Patient has {bp_category}."
                if bp_category == "Hypertensive Crisis":
                    result['recommendations'].append("Immediate medical attention required.")
                elif bp_category in ["Stage 1 Hypertension", "Stage 2 Hypertension"]:
                    result['recommendations'].append("Consider anti-hypertensive medications.")
                    result['recommendations'].append("Recommend lifestyle modifications including diet and exercise.")
                else:
                    result['recommendations'].append("Recommend lifestyle modifications and monitoring.")
            else:
                result['interpretation'] = "Blood pressure is within normal range."
                
        elif test_name == "Basic Blood Test":
            # Generate blood test results
            condition = None
            if is_abnormal:
                # If we expect abnormal results, pick a condition based on symptoms
                if "Fever" in self.current_symptoms or "Cough" in self.current_symptoms:
                    condition = "infection"
                elif "Shortness of Breath" in self.current_symptoms or "Chest Pain" in self.current_symptoms:
                    condition = "cardiac"
                elif "Fatigue" in self.current_symptoms or "Headache" in self.current_symptoms:
                    condition = "anemia"
                else:
                    # Random abnormality
                    condition = random.choice(["infection", "anemia", "dehydration", "liver", "kidney"])
            
            # Create simulated blood test results
            blood_results = {
                'WBC': {'value': random.uniform(4.5, 11.0), 'unit': 'x10^9/L', 'reference_range': '4.5-11.0'},
                'RBC': {'value': random.uniform(4.2, 5.8), 'unit': 'x10^12/L', 'reference_range': '4.2-5.8'},
                'Hemoglobin': {'value': random.uniform(13.5, 17.5), 'unit': 'g/dL', 'reference_range': '13.5-17.5'},
                'Platelets': {'value': random.uniform(150, 400), 'unit': 'x10^9/L', 'reference_range': '150-400'},
                'Glucose': {'value': random.uniform(70, 100), 'unit': 'mg/dL', 'reference_range': '70-100'}
            }
            
            # If we have the image generator available, use it for more detailed results
            if has_image_generator:
                try:
                    blood_results = ImageGenerator.generate_blood_test_results(self.patient_id, condition)
                except Exception as e:
                    print(f"Error generating blood test results: {e}")
            
            # Extract the most important values for the details
            result['details'] = {
                'wbc': f"{blood_results['WBC']['value']:.1f} {blood_results['WBC']['unit']}",
                'rbc': f"{blood_results['RBC']['value']:.1f} {blood_results['RBC']['unit']}",
                'hemoglobin': f"{blood_results['Hemoglobin']['value']:.1f} {blood_results['Hemoglobin']['unit']}",
                'platelets': f"{blood_results['Platelets']['value']:.1f} {blood_results['Platelets']['unit']}",
                'glucose': f"{blood_results['Glucose']['value']:.1f} {blood_results['Glucose']['unit']}"
            }
            
            # Store full results in the test_data field
            full_results = {k: v for k, v in blood_results.items() if k not in ['patient_id', 'timestamp']}
            result['full_results'] = full_results
            
            # Generate interpretation based on abnormal values
            abnormal_values = []
            for test, data in full_results.items():
                if isinstance(data, dict) and data.get('abnormal', False):
                    direction = data.get('direction', '')
                    abnormal_values.append(f"{test} is {direction} ({data['value']:.1f} {data['unit']})")
            
            if abnormal_values:
                result['is_abnormal'] = True
                result['interpretation'] = "Abnormal blood test results: " + ", ".join(abnormal_values[:3])
                if len(abnormal_values) > 3:
                    result['interpretation'] += f", and {len(abnormal_values) - 3} more abnormalities."
                
                # Add recommendations
                if any('WBC' in val for val in abnormal_values):
                    result['recommendations'].append("Consider infection workup.")
                if any('Hemoglobin' in val for val in abnormal_values) or any('RBC' in val for val in abnormal_values):
                    result['recommendations'].append("Evaluate for anemia or blood loss.")
                if any('Glucose' in val for val in abnormal_values):
                    result['recommendations'].append("Check for diabetes or metabolic disorders.")
            else:
                result['interpretation'] = "Blood test results are within normal ranges."
                
        elif test_name == "ECG/EKG":
            # Determine if ECG should be abnormal based on symptoms
            is_abnormal_ecg = is_abnormal or "Chest Pain" in self.current_symptoms
            
            # Initialize with basic info
            ecg_image_path = None
            
            # Generate ECG image if image generator is available
            if has_image_generator:
                try:
                    ecg_image_path = ImageGenerator.generate_ecg(
                        self.patient_id,
                        self.vital_signs.pulse,
                        abnormal=is_abnormal_ecg
                    )
                except Exception as e:
                    print(f"Error generating ECG image: {e}")
            
            # Get interpretation
            if is_abnormal_ecg:
                # Simulate an abnormal finding
                if "Chest Pain" in self.current_symptoms:
                    interpretation = random.choice([
                        "ST segment elevation suggestive of myocardial infarction.",
                        "ST depression indicating possible ischemia.",
                        "T wave inversion in leads V3-V5, concerning for ischemia.",
                        "Prolonged QT interval, requiring further evaluation."
                    ])
                    
                    # Add recommendations
                    result['recommendations'].append("Consider cardiac enzymes.")
                    result['recommendations'].append("Cardiology consultation recommended.")
                    if "ST segment elevation" in interpretation:
                        result['recommendations'].append("Urgent cardiac catheterization may be indicated.")
                else:
                    interpretation = random.choice([
                        "Non-specific ST-T wave changes.",
                        "Sinus tachycardia.",
                        "Premature ventricular contractions (PVCs).",
                        "Left ventricular hypertrophy pattern."
                    ])
                    
                    result['recommendations'].append("Consider cardiac follow-up if clinically indicated.")
            else:
                interpretation = "Normal sinus rhythm with no acute ST-T wave changes."
            
            result['details'] = {
                'heart_rate': f"{self.vital_signs.pulse} BPM",
                'rhythm': "Regular" if not is_abnormal_ecg else "Irregular" if random.random() < 0.5 else "Regular",
                'intervals': "Normal" if not is_abnormal_ecg else "Abnormal"
            }
            
            # Add image path if available
            if ecg_image_path:
                result['details']['image_path'] = ecg_image_path
            
            result['interpretation'] = interpretation
            result['is_abnormal'] = is_abnormal_ecg
            
        elif test_name == "Chest X-Ray":
            # Determine if X-ray should be abnormal based on symptoms
            is_abnormal_xray = is_abnormal or "Shortness of Breath" in self.current_symptoms or "Chest Pain" in self.current_symptoms
            
            # Determine condition for abnormal X-ray
            condition = None
            if is_abnormal_xray:
                if "Cough" in self.current_symptoms and "Fever" in self.current_symptoms:
                    condition = "pneumonia"
                elif "Chest Pain" in self.current_symptoms:
                    if random.random() < 0.5:
                        condition = "cardiac"
                    else:
                        condition = "fracture"
                elif "Shortness of Breath" in self.current_symptoms:
                    condition = "cardiac" if random.random() < 0.7 else "pneumonia"
            
            # Initialize with empty image path
            xray_image_path = None
            
            # Generate X-ray image if image generator is available
            if has_image_generator:
                try:
                    xray_image_path = ImageGenerator.generate_chest_xray(
                        self.patient_id,
                        condition=condition
                    )
                except Exception as e:
                    print(f"Error generating X-ray image: {e}")
            
            # Get interpretation text
            if is_abnormal_xray and condition:
                if condition == "pneumonia":
                    interpretation = random.choice([
                        "Opacity in the right lower lobe consistent with pneumonia.",
                        "Left upper lobe infiltrate suggesting pneumonic process.",
                        "Bilateral patchy infiltrates consistent with pneumonia."
                    ])
                    
                    # Add recommendations
                    result['recommendations'].append("Consider antibiotic therapy.")
                    result['recommendations'].append("Follow-up imaging in 2-4 weeks to confirm resolution.")
                elif condition == "fracture":
                    interpretation = random.choice([
                        "Fracture of the 7th rib on the right side.",
                        "Acute fracture of the left 5th rib without displacement.",
                        "Minimally displaced fracture of the right 8th rib."
                    ])
                    
                    result['recommendations'].append("Pain management as needed.")
                    result['recommendations'].append("Consider orthopedic consultation for rib fractures.")
                elif condition == "cardiac":
                    interpretation = random.choice([
                        "Cardiomegaly with cardiothoracic ratio of 0.65.",
                        "Enlarged cardiac silhouette suggesting cardiomegaly.",
                        "Mild pulmonary vascular congestion suggesting heart failure."
                    ])
                    
                    result['recommendations'].append("Cardiology consultation recommended.")
                    result['recommendations'].append("Consider echocardiogram for further evaluation.")
                else:
                    interpretation = "Abnormal finding of uncertain etiology."
            else:
                interpretation = random.choice([
                    "No significant abnormalities detected.",
                    "Findings within normal limits.",
                    "Normal examination with no pathological findings."
                ])
            
            result['details'] = {
                'findings': interpretation,
                'quality': "Good" if random.random() < 0.8 else "Limited due to patient positioning"
            }
            
            # Add image path if available
            if xray_image_path:
                result['details']['image_path'] = xray_image_path
            
            result['interpretation'] = interpretation
            result['is_abnormal'] = is_abnormal_xray and condition is not None
            
        elif test_name == "Pulmonary Function Test":
            # Generate pulmonary function results
            normal_fev1 = 3.5  # normal forced expiratory volume in 1 second (L)
            normal_fvc = 4.5   # normal forced vital capacity (L)
            
            # Modify based on symptoms
            if "Shortness of Breath" in self.current_symptoms or is_abnormal:
                fev1 = normal_fev1 * random.uniform(0.5, 0.8)  # reduced
                fvc = normal_fvc * random.uniform(0.6, 0.9)    # reduced
                interpretation = random.choice([
                    "Moderate obstructive pattern consistent with asthma or COPD.",
                    "Restrictive pattern suggesting interstitial lung disease.",
                    "Mixed obstructive and restrictive pattern."
                ])
                result['is_abnormal'] = True
                
                # Add recommendations
                result['recommendations'].append("Consider bronchodilator therapy.")
                result['recommendations'].append("Chest imaging recommended.")
                if "obstructive" in interpretation:
                    result['recommendations'].append("Consider inhaled corticosteroids.")
            else:
                fev1 = normal_fev1 * random.uniform(0.9, 1.1)  # normal
                fvc = normal_fvc * random.uniform(0.9, 1.1)    # normal
                interpretation = "Normal pulmonary function with no evidence of obstruction or restriction."
            
            fev1_fvc_ratio = (fev1 / fvc) * 100
            
            result['details'] = {
                'fev1': f"{fev1:.2f} L ({int(fev1/normal_fev1*100)}% predicted)",
                'fvc': f"{fvc:.2f} L ({int(fvc/normal_fvc*100)}% predicted)",
                'fev1_fvc_ratio': f"{fev1_fvc_ratio:.1f}%",
                'dlco': f"{random.uniform(70, 100) if not result['is_abnormal'] else random.uniform(40, 70):.1f}% predicted"
            }
            
            result['interpretation'] = interpretation
            
        elif test_name == "Physical Examination":
            result['details'] = {
                'general_appearance': 'Alert and oriented' if self.condition_severity < 5 else 'Distressed',
                'skin': 'Normal' if self.condition_severity < 4 else 'Pale and clammy',
                'lungs': 'Clear' if 'Shortness of Breath' not in self.current_symptoms else 'Wheezing noted',
                'heart': 'Regular rhythm' if 'Chest Pain' not in self.current_symptoms else 'Irregular rhythm',
                'abdomen': 'Soft' if 'Abdominal Pain' not in self.current_symptoms else 'Tender to palpation'
            }
            
            if self.condition_severity > 3:
                result['is_abnormal'] = True
                result['interpretation'] = "Abnormal examination findings"
                
        elif test_name == "Basic Blood Test":
            # Generate blood test values based on symptoms and condition
            wbc = 7.5  # Normal: 4.5-11.0
            rbc = 4.8  # Normal: 4.5-5.5
            hgb = 14.0  # Normal: 13.5-17.5
            hct = 42.0  # Normal: 41-50
            plt = 250.0  # Normal: 150-450
            
            # Adjust values based on conditions
            if 'Fever' in self.current_symptoms:
                wbc += random.uniform(3.0, 7.0)  # Elevated WBC in infection
            
            if 'Fatigue' in self.current_symptoms:
                hgb -= random.uniform(2.0, 4.0)  # Lower hemoglobin in anemia
                hct -= random.uniform(5.0, 8.0)
            
            result['details'] = {
                'WBC': f"{wbc:.1f} x10^9/L",
                'RBC': f"{rbc:.1f} x10^12/L",
                'Hemoglobin': f"{hgb:.1f} g/dL",
                'Hematocrit': f"{hct:.1f}%",
                'Platelets': f"{plt:.0f} x10^9/L"
            }
            
            # Flag abnormal results
            abnormal_values = []
            if wbc > 11.0:
                abnormal_values.append("Elevated WBC - possible infection or inflammation")
            if hgb < 13.5:
                abnormal_values.append("Low hemoglobin - possible anemia")
            
            if abnormal_values:
                result['is_abnormal'] = True
                result['interpretation'] = "; ".join(abnormal_values)
                
        elif test_name == "ECG/EKG":
            # Generate ECG results based on heart-related symptoms
            rhythm = "Normal sinus rhythm"
            rate = self.vital_signs.pulse
            intervals = "Normal"
            st_changes = "None"
            
            if 'Chest Pain' in self.current_symptoms:
                if self.condition_severity >= 7:
                    rhythm = "Sinus tachycardia with ST elevation"
                    st_changes = "ST elevation in leads V1-V5"
                    result['is_abnormal'] = True
                    result['interpretation'] = "Findings consistent with myocardial ischemia/infarction"
                elif self.condition_severity >= 5:
                    rhythm = "Sinus tachycardia with ST depression"
                    st_changes = "ST depression in leads II, III, aVF"
                    result['is_abnormal'] = True
                    result['interpretation'] = "Findings suggestive of myocardial ischemia"
            
            result['details'] = {
                'Rhythm': rhythm,
                'Rate': f"{rate} BPM",
                'Intervals': intervals,
                'ST Changes': st_changes
            }
                
        elif test_name == "Blood Pressure":
            systolic = self.vital_signs.systolic_bp
            diastolic = self.vital_signs.diastolic_bp
            
            result['details'] = {
                'Systolic': f"{systolic} mmHg",
                'Diastolic': f"{diastolic} mmHg",
                'Mean Arterial Pressure': f"{int((2*diastolic + systolic)/3)} mmHg"
            }
            
            if systolic >= 140 or diastolic >= 90:
                result['is_abnormal'] = True
                result['interpretation'] = "Hypertension"
            elif systolic <= 90 or diastolic <= 60:
                result['is_abnormal'] = True
                result['interpretation'] = "Hypotension"
                
        elif test_name == "Urinalysis":
            # Generate urinalysis results
            glucose = "Negative"
            blood = "Negative"
            protein = "Negative"
            nitrites = "Negative"
            leukocytes = "Negative"
            
            # Modify based on conditions
            if self.condition_severity > 5:
                if random.random() > 0.5:
                    blood = "Positive"
                    result['is_abnormal'] = True
                if random.random() > 0.7:
                    protein = "Trace"
                    result['is_abnormal'] = True
            
            result['details'] = {
                'Color': 'Yellow',
                'Clarity': 'Clear',
                'Specific Gravity': '1.010',
                'pH': '6.0',
                'Glucose': glucose,
                'Blood': blood,
                'Protein': protein,
                'Nitrites': nitrites,
                'Leukocytes': leukocytes
            }
            
            if result['is_abnormal']:
                result['interpretation'] = "Abnormal urinalysis findings"
                
        elif test_name == "Chest X-Ray":
            # Generate X-ray results based on respiratory symptoms
            finding = "Normal lung fields bilaterally. No cardiomegaly."
            
            if 'Shortness of Breath' in self.current_symptoms or 'Cough' in self.current_symptoms:
                if self.condition_severity >= 6:
                    finding = "Bilateral infiltrates present. Possible pneumonia."
                    result['is_abnormal'] = True
                    result['interpretation'] = "Findings consistent with pneumonia"
                elif self.condition_severity >= 4:
                    finding = "Mild interstitial changes noted in right lower lobe."
                    result['is_abnormal'] = True
                    result['interpretation'] = "Possible early pulmonary infection or inflammation"
            
            result['details'] = {
                'Findings': finding,
                'Heart Size': 'Normal' if 'Heart Failure' not in self.medical_history else 'Enlarged',
                'Lung Fields': 'Clear' if not result['is_abnormal'] else 'Abnormal'
            }
        
        else:
            # Generic test result for tests not specifically implemented
            result['details'] = {
                'Test Completed': 'Yes',
                'Quality': 'Good'
            }
            
            # Random abnormality based on condition severity
            if random.random() < (self.condition_severity / 10):
                result['is_abnormal'] = True
                result['interpretation'] = f"Abnormal findings on {test_name}"
        
        return result
    
    def update_condition(self, severity_change: int) -> None:
        """
        Update the patient's condition severity.
        
        Args:
            severity_change: Positive or negative change to condition severity
        """
        new_severity = self.condition_severity + severity_change
        self.condition_severity = max(1, min(10, new_severity))  # Keep between 1-10
        
        # Update vital signs based on condition change
        # Simple algorithm for Phase 1 - will be more sophisticated in later phases
        if severity_change > 0:  # Condition worsening
            pulse_change = random.randint(5, 15)
            bp_change = random.randint(5, 15)
            self.vital_signs.update_vitals(
                pulse=self.vital_signs.pulse + pulse_change,
                systolic_bp=self.vital_signs.systolic_bp + bp_change,
                diastolic_bp=self.vital_signs.diastolic_bp + bp_change // 2,
                oxygen_saturation=max(70, self.vital_signs.oxygen_saturation - random.randint(1, 5))
            )
        elif severity_change < 0:  # Condition improving
            pulse_change = random.randint(5, 10)
            bp_change = random.randint(5, 10)
            self.vital_signs.update_vitals(
                pulse=max(60, self.vital_signs.pulse - pulse_change),
                systolic_bp=max(90, self.vital_signs.systolic_bp - bp_change),
                diastolic_bp=max(60, self.vital_signs.diastolic_bp - bp_change // 2),
                oxygen_saturation=min(100, self.vital_signs.oxygen_saturation + random.randint(1, 3))
            )
    
    def is_critical(self) -> bool:
        """Check if patient is in critical condition based on vital signs."""
        return (self.condition_severity >= 8 or
                self.vital_signs.pulse > 120 or self.vital_signs.pulse < 50 or
                self.vital_signs.systolic_bp > 180 or self.vital_signs.systolic_bp < 90 or
                self.vital_signs.oxygen_saturation < 90)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Patient':
        """
        Create a Patient instance from a dictionary.
        Useful for loading from JSON or database.
        
        Args:
            data: Dictionary containing patient data
            
        Returns:
            Patient instance
        """
        vital_signs = None
        if 'vital_signs' in data:
            v = data['vital_signs']
            vital_signs = VitalSigns(
                pulse=v.get('pulse', 80),
                systolic_bp=v.get('systolic_bp', 120),
                diastolic_bp=v.get('diastolic_bp', 80),
                temperature=v.get('temperature', 36.6),
                respiratory_rate=v.get('respiratory_rate', 16),
                oxygen_saturation=v.get('oxygen_saturation', 98)
            )
        
        return cls(
            patient_id=data.get('patient_id', ''),
            name=data.get('name', ''),
            age=data.get('age', 30),
            gender=data.get('gender', ''),
            medical_history=data.get('medical_history', []),
            current_symptoms=data.get('current_symptoms', []),
            vital_signs=vital_signs,
            diagnosis=data.get('diagnosis', None),
            condition_severity=data.get('condition_severity', 1)
        )
