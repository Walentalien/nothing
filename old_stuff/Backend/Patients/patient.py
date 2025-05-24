from Backend.Medications.medications import MedicationType
from Backend.Tests.biochemistry import BiochemistryTests
from Backend.Tests.hematology import BloodTest

#pain_level [0-10]

class Patient:
    def __init__(self,name: str, age: int, gender: str):
        self.name = name
        self.age = age
        self.gender = gender
        self.parameters = {
            "pulse": 80,
            "systolic_pressure": 50,
            "diastolic_pressure": 100,
            "temperature": 35.6,
            "weight": 70,
            "height": 170,
            "sp_o2": 98,
            "symptoms": {
        # Skale (0–10)
        "pain_level": 0,
        "infection_level": 0,
        "inflammation_level": 0,
        "breath_difficulty_level": 0,
        "nausea_level": 0,
        "anxiety_level": 0,

        # Objawy obecne/nieobecne
        "vomiting": False,
        "diarrhea": False,
        "constipation": False,
        "cough": False,
        "productive_cough": False,
        "shortness_of_breath": False,
        "chest_pain": False,
        "headache": False,
        "dizziness": False,
        "syncope": False,                 # omdlenie
        "fever": False,
        "chills": False,
        "sore_throat": False,
        "runny_nose": False,
        "nasal_congestion": False,
        "loss_of_smell": False,
        "loss_of_taste": False,
        "joint_pain": False,
        "muscle_ache": False,
        "skin_rash": False,
        "itchiness": False,
        "swelling": False,
        "bleeding": False,
        "urinary_pain": False,
        "frequent_urination": False,
        "vision_blur": False,
        "hearing_loss": False,
        "sleep_disturbance": False,
        "appetite_loss": False,
        "weight_loss": False,
        "weight_gain": False
}

        }
        self.medical_history = []
        self.allergies = []
        self.medications = []
        self.blood_parameters = {blood: None for blood in BloodTest}
        self.biochemistry = {bio: None for bio in BiochemistryTests}
        self.urine = {urine: None for urine in UrineTests}

# pulse/pressure/temperature/weight/height/sp_o2 -- const parameters for all patients
# Adding a symptom like headache etc
    def set_parameters(self, pulse, systolic_pressure, diastolic_pressure, temperature,weight, height, sp_o2):
        self.parameters["pulse"] = pulse
        self.parameters["systolic_pressure"] = systolic_pressure
        self.parameters["diastolic_pressure"] = diastolic_pressure
        self.parameters["temperature"] = temperature
        self.parameters["weight"] = weight
        self.parameters["height"] = height
        self.parameters["sp_o2"] = sp_o2

    def add_medical_history(self, medical_history: list):
        self.medical_history.append(medical_history)

    def add_allergies(self, allergen: str):
        self.allergies.append(allergen)


    def get_parameters(self):
        return self.parameters

    def bmi(self):
       height_in_meters = self.parameters["height"] / 100
       return self.parameters["weight"] / (height_in_meters ** 2)

    def add_symptoms(self,symptom_name,details):
        self.parameters["symptoms"][symptom_name] = details

    def pulse_analyze(self):
        if self.parameters["pulse"] > 100:
            return "Tachycardia"
        elif self.parameters["pulse"] < 60:
            return "Bradycardia"
        else:
            return "Normal heart rate"


    def temperature_analyze(self):
        if 38.0 > self.parameters["temperature"] > 37.1:
            return "mild fever"
        elif self.parameters["temperature"] >= 38.0:
            return "fever"
        elif self.parameters["temperature"] < 35.5:
            return "hypothermia"
        else:
            return "normal temperature"

    def sp_o2_analyze(self):
        if self.parameters["sp_o2"] >= 95:
            return "Normal"
        elif 90 <= self.parameters["sp_o2"] < 95:
            return "Mild Hypoxia"
        elif 85 <= self.parameters["sp_o2"] < 90:
            return "Moderate Hypoxia"
        else:
            return "Severe Hypoxia"

    def pressure_analyze(self):
        if self.parameters["systolic_pressure"] < 120 and self.parameters["diastolic_pressure"] <80:
            return "Optimal"
        elif 120 <= self.parameters["systolic_pressure"] <= 129 or 80 <= self.parameters["diastolic_pressure"] <= 84:
            return "Normal"
        elif 130 <= self.parameters["systolic_pressure"] <= 139 or 85 <= self.parameters["diastolic_pressure"] <= 89:
            return "High Normal"
        elif 140 <= self.parameters["systolic_pressure"] <= 159 or 90 <= self.parameters["diastolic_pressure"] <= 99:
            return "Hypertension Stage 1"
        elif 160 <= self.parameters["systolic_pressure"] <= 179 or 100 <= self.parameters["diastolic_pressure"] <= 109:
            return "Hypertension Stage 2"
        elif self.parameters["systolic_pressure"] >= 180 or self.parameters["diastolic_pressure"] >= 110:
            return "Hypertension Stage 3"
        elif self.parameters["systolic_pressure"] >= 140 and self.parameters["diastolic_pressure"] < 90:
            return "Isolated Systolic Hypertension"
        else:
            return "Undefined"


    def apply_medications(self, medication: MedicationType):
        effects = {
        MedicationType.BETA_BLOCKER: {
             self.parameters["pulse"]: -10,
             self.parameters["systolic_pressure"]: -10,
             self.parameters["diastolic_pressure"]: -5
        },
        MedicationType.ACE_INHIBITOR: {
            self.parameters["systolic_pressure"]: -8,
            self.parameters["diastolic_pressure"]: -5
        },
        MedicationType.CALCIUM_CHANNEL_BLOCKER: {
            self.parameters["systolic_pressure"]: -6,
            self.parameters["diastolic_pressure"]: -4
        },
        MedicationType.VASOPRESSOR: {
            self.parameters["systolic_pressure"]: +15,
            self.parameters["diastolic_pressure"]: +10
        },
        MedicationType.DIURETIC: {
            self.parameters["systolic_pressure"]: -8,
            self.parameters["diastolic_pressure"]: -4,
            self.parameters["weight"]: -1
        },
        MedicationType.NITRATES: {
            self.parameters["systolic_pressure"]: -12,
            self.parameters["diastolic_pressure"]: -8
        },
        MedicationType.PARACETAMOL: {
            self.parameters["temperature"]: -1.0
        },

    }















