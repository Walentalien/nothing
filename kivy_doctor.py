"""
VirtualDoctor - Kivy GUI Version
A medical simulation game with graphical interface
"""

import os
import random
import json
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.spinner import Spinner

# Create directories if they don't exist
os.makedirs('data/images', exist_ok=True)

# Import our models
from models.patient import Patient, VitalSigns
from utils.image_generator import ImageGenerator
from models.doctor import Doctor, get_available_specializations
from models.diagnosis import diagnosis_catalog
from utils.db_manager import DBManager
from utils.game_state import GameState

# Set some global parameters
Window.size = (800, 600)
Window.clearcolor = (0.9, 0.9, 0.9, 1)

# Fix font rendering
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path

# Add fonts directory to resources
resource_add_path(os.path.join(os.path.dirname(__file__), 'assets/fonts'))

# Try to register default system fonts if they exist
try:
    # Common font locations by OS
    font_locations = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',      # Linux
        '/System/Library/Fonts/Helvetica.ttc',                  # macOS
        'C:/Windows/Fonts/Arial.ttf',                           # Windows
        os.path.join(os.path.dirname(__file__), 'assets/fonts/DejaVuSans.ttf')  # Custom location
    ]
    
    # Try to register the first font that exists
    for font_path in font_locations:
        if os.path.exists(font_path):
            LabelBase.register('Roboto', font_path)
            break
except Exception as e:
    print(f"Warning: Could not register custom font: {e}")

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        
        from kivy.graphics import Color, Rectangle
        
        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Add title with background
        title_box = BoxLayout(size_hint_y=0.15)
        with title_box.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Medical blue
            self.rect = Rectangle(pos=title_box.pos, size=title_box.size)
        title_box.bind(pos=self.update_rect, size=self.update_rect)
        
        title = Label(
            text="VirtualDoctor",
            font_size=32,
            color=(1, 1, 1, 1),
            bold=True
        )
        title_box.add_widget(title)
        layout.add_widget(title_box)
        
        # Add subtitle
        subtitle = Label(
            text="Medical Simulation Game",
            font_size=20,
            color=(0.3, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(subtitle)
        
        # Add image - we'll use a placeholder
        logo = Image(
            # source='assets/logo.png' if os.path.exists('assets/logo.png') else None,
            source='generated-icon.png' if os.path.exists('generated-icon.png') else None,
            size_hint_y=None,
            height=dp(200)
        )
        layout.add_widget(logo)
        
        # User status section
        self.user_status_label = Label(
            text="Not logged in",
            font_size=16,
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(self.user_status_label)
        
        # Add buttons
        btn_start = Button(
            text="Start Doctor Mode",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_start.bind(on_press=self.go_to_specialization)
        layout.add_widget(btn_start)
        
        # Login/Dashboard button
        self.login_button = Button(
            text="Login / Register",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.3, 0.7, 0.4, 1)
        )
        self.login_button.bind(on_press=self.go_to_login)
        layout.add_widget(self.login_button)
        
        btn_about = Button(
            text="About",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.3, 0.3, 0.3, 1)
        )
        btn_about.bind(on_press=self.go_to_about)
        layout.add_widget(btn_about)
        
        btn_quit = Button(
            text="Quit",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        btn_quit.bind(on_press=self.quit_app)
        layout.add_widget(btn_quit)
        
        # Add a spacer
        layout.add_widget(Label(size_hint_y=None, height=dp(30)))
        
        self.add_widget(layout)
    
    def update_rect(self, instance, value):
        """Update rectangle position and size"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def go_to_specialization(self, instance):
        self.manager.get_screen('specialization').reset()
        self.manager.current = 'specialization'
    
    def go_to_login(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'current_user') and app.current_user:
            # If already logged in, go to dashboard
            self.manager.get_screen('dashboard').update_for_user(app.current_user)
            self.manager.transition.direction = 'left'
            self.manager.current = 'dashboard'
        else:
            # If not logged in, go to login screen
            self.manager.transition.direction = 'left'
            self.manager.current = 'login'
    
    def go_to_about(self, instance):
        self.manager.current = 'about'
    
    def quit_app(self, instance):
        App.get_running_app().stop()
        
    def update_for_logged_user(self, user):
        """Update the UI when a user is logged in"""
        if user:
            self.user_status_label.text = f"Logged in as: {user['username']}"
            self.login_button.text = "My Dashboard"
        else:
            self.user_status_label.text = "Not logged in"
            self.login_button.text = "Login / Register"


class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Add title
        title = Label(
            text="About VirtualDoctor",
            font_size=24,
            size_hint_y=None,
            height=dp(40),
            color=(0.2, 0.2, 0.2, 1), #Dark gray text
        )
        layout.add_widget(title)
        
        # Add scrollable text area
        scroll_view = ScrollView(size_hint=(1, 1))
        text_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        text_grid.bind(minimum_height=text_grid.setter('height'))
        
        about_text = """
VirtualDoctor is an educational medical simulation game designed to help medical students and healthcare professionals practice diagnostic and treatment skills in a risk-free virtual environment.

Features:
• Choose from multiple medical specializations
• Diagnose and treat virtual patients with realistic symptoms
• View medical imaging including ECGs and X-rays
• Analyze blood test results and other diagnostics
• Make diagnoses based on patient symptoms and test results
• Monitor your performance and accuracy

Phase 3 Enhancements:
• Advanced medical imaging with dynamically generated ECGs and X-rays
• Detailed database for patient records and medical history
• Enhanced test results with clinical recommendations
• Improved diagnosis matching using test results and symptoms

This application was developed as an educational tool and should not replace actual medical training or professional medical advice.
        """
        
        about_label = Label(
            text=about_text,
            font_size=14,
            size_hint_y=None,
            text_size=(Window.width - dp(60), None),
            halign='left',
            valign='top',
            color=(0.2, 0.2, 0.2, 1) #Dark gray text
        )
        about_label.bind(texture_size=about_label.setter('size'))
        text_grid.add_widget(about_label)
        scroll_view.add_widget(text_grid)
        layout.add_widget(scroll_view)
        
        # Add button to return to main menu
        btn_back = Button(
            text="Back to Main Menu",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_back.bind(on_press=self.go_to_main)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def go_to_main(self, instance):
        self.manager.current = 'main_menu'


class SpecializationScreen(Screen):
    def __init__(self, **kwargs):
        super(SpecializationScreen, self).__init__(**kwargs)
        self.game_state = App.get_running_app().game_state
        self.specializations = get_available_specializations()
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Add title
        title = Label(
            text="Select Your Specialization",
            font_size=24,
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(title)
        
        # Add instructions
        instructions = Label(
            text="Choose a medical specialty that determines your available tests and treatments",
            font_size=14,
            size_hint_y=None,
            height=dp(30)
        )
        layout.add_widget(instructions)
        
        # Create a scrollview for specializations
        scroll_view = ScrollView(size_hint=(1, 1))
        self.specialization_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.specialization_layout.bind(minimum_height=self.specialization_layout.setter('height'))
        scroll_view.add_widget(self.specialization_layout)
        layout.add_widget(scroll_view)
        
        # Add buttons for each specialization
        self.populate_specializations()
        
        # Add button to return to main menu
        btn_back = Button(
            text="Back to Main Menu",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_back.bind(on_press=self.go_to_main)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def populate_specializations(self):
        self.specialization_layout.clear_widgets()
        
        for specialization in self.specializations:
            spec_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(150), padding=5)
            spec_box.background_color = (0.95, 0.95, 0.95, 1)
            
            # Add name
            name_label = Label(
                text=specialization.name,
                font_size=18,
                size_hint_y=None,
                height=dp(30),
                color=(0.2, 0.2, 0.8, 1)
            )
            spec_box.add_widget(name_label)
            
            # Add description
            desc_label = Label(
                text=specialization.description,
                font_size=14,
                size_hint_y=None,
                height=dp(40),
                text_size=(Window.width - dp(60), None),
                halign='left'
            )
            spec_box.add_widget(desc_label)
            
            # Add available tests
            tests_label = Label(
                text="Tests: " + ", ".join(specialization.available_tests[:3]) + "...",
                font_size=12,
                size_hint_y=None,
                height=dp(20),
                text_size=(Window.width - dp(60), None),
                halign='left'
            )
            spec_box.add_widget(tests_label)
            
            # Add available treatments
            treatments_label = Label(
                text="Treatments: " + ", ".join(specialization.available_treatments[:3]) + "...",
                font_size=12,
                size_hint_y=None,
                height=dp(20),
                text_size=(Window.width - dp(60), None),
                halign='left'
            )
            spec_box.add_widget(treatments_label)
            
            # Add selection button
            select_btn = Button(
                text="Select",
                size_hint_y=None,
                height=dp(40),
                background_color=(0.2, 0.6, 0.8, 1)
            )
            select_btn.specialization = specialization
            select_btn.bind(on_press=self.select_specialization)
            spec_box.add_widget(select_btn)
            
            self.specialization_layout.add_widget(spec_box)
    
    def select_specialization(self, instance):
        specialization = instance.specialization
        doctor = Doctor("Doctor", specialization=specialization)
        self.game_state.set_doctor(doctor)
        
        # Load a random patient
        self.game_state.load_random_patient()
        
        # Go to patient view
        self.manager.get_screen('patient').update_patient_data()
        self.manager.current = 'patient'
    
    def go_to_main(self, instance):
        self.manager.current = 'main_menu'
    
    def reset(self):
        App.get_running_app().game_state.reset_game()


class PatientScreen(Screen):
    def __init__(self, **kwargs):
        super(PatientScreen, self).__init__(**kwargs)
        self.game_state = App.get_running_app().game_state
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Top panel with patient info and vitals
        top_panel = BoxLayout(orientation='horizontal', size_hint_y=0.4, spacing=10)
        
        # Patient info
        self.patient_info = BoxLayout(orientation='vertical', size_hint_x=0.5)
        self.patient_name = Label(font_size=20, halign='left', valign='top', text_size=(Window.width/2 - dp(20), None))
        self.patient_info.add_widget(self.patient_name)
        
        self.patient_details = Label(font_size=14, halign='left', valign='top', text_size=(Window.width/2 - dp(20), None))
        self.patient_info.add_widget(self.patient_details)
        
        self.patient_history = Label(font_size=14, halign='left', valign='top', text_size=(Window.width/2 - dp(20), None))
        self.patient_info.add_widget(self.patient_history)
        
        top_panel.add_widget(self.patient_info)
        
        # Vital signs
        vitals_panel = BoxLayout(orientation='vertical', size_hint_x=0.5)
        vitals_title = Label(text="Vital Signs", font_size=18, size_hint_y=0.2)
        vitals_panel.add_widget(vitals_title)
        
        vitals_grid = GridLayout(cols=2, size_hint_y=0.8)
        self.vital_labels = {}
        for vital in ["Heart Rate", "Blood Pressure", "Temperature", "Respiratory Rate", "O₂ Saturation"]:
            vitals_grid.add_widget(Label(text=vital, halign='left', text_size=(Window.width/4 - dp(20), None)))
            label = Label(text="--", halign='left', text_size=(Window.width/4 - dp(20), None))
            vitals_grid.add_widget(label)
            self.vital_labels[vital] = label
        
        vitals_panel.add_widget(vitals_grid)
        top_panel.add_widget(vitals_panel)
        
        layout.add_widget(top_panel)
        
        # Middle panel with symptoms
        middle_panel = BoxLayout(orientation='vertical', size_hint_y=0.2)
        symptoms_title = Label(text="Current Symptoms", font_size=18, size_hint_y=0.3)
        middle_panel.add_widget(symptoms_title)
        
        self.symptoms_label = Label(
            text="No symptoms reported",
            font_size=16,
            halign='center',
            valign='middle',
            size_hint_y=0.7
        )
        middle_panel.add_widget(self.symptoms_label)
        
        layout.add_widget(middle_panel)
        
        # Action buttons
        actions_panel = BoxLayout(orientation='horizontal', size_hint_y=0.3, spacing=10)
        
        btn_tests = Button(
            text="Run Tests",
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_tests.bind(on_press=self.show_tests)
        actions_panel.add_widget(btn_tests)
        
        btn_treatments = Button(
            text="Administer Treatments",
            background_color=(0.2, 0.8, 0.2, 1)
        )
        btn_treatments.bind(on_press=self.show_treatments)
        actions_panel.add_widget(btn_treatments)
        
        btn_medications = Button(
            text="Administer Medications",
            background_color=(0.8, 0.2, 0.8, 1)
        )
        btn_medications.bind(on_press=self.show_medications)
        actions_panel.add_widget(btn_medications)
        
        btn_diagnose = Button(
            text="Make Diagnosis",
            background_color=(0.8, 0.6, 0.2, 1)
        )
        btn_diagnose.bind(on_press=self.show_diagnosis)
        actions_panel.add_widget(btn_diagnose)
        
        layout.add_widget(actions_panel)
        
        # Bottom panel with navigation
        bottom_panel = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)
        
        btn_main = Button(
            text="Return to Menu",
            background_color=(0.8, 0.2, 0.2, 1)
        )
        btn_main.bind(on_press=self.go_to_main)
        bottom_panel.add_widget(btn_main)
        
        btn_next = Button(
            text="Next Patient",
            background_color=(0.6, 0.6, 0.6, 1)
        )
        btn_next.bind(on_press=self.next_patient)
        bottom_panel.add_widget(btn_next)
        
        layout.add_widget(bottom_panel)
        
        self.add_widget(layout)
    
    def update_patient_data(self):
        if not self.game_state.current_patient:
            self.patient_name.text = "No patient loaded"
            return
        
        patient = self.game_state.current_patient
        
        # Update patient info
        self.patient_name.text = f"Patient: {patient.name}"
        self.patient_details.text = f"Age/Gender: {patient.age} years, {patient.gender}\nCondition: {self.get_condition_text(patient.condition_severity)}"
        
        history_text = "Medical History: "
        if patient.medical_history:
            history_text += ", ".join(patient.medical_history)
        else:
            history_text += "None"
        self.patient_history.text = history_text
        
        # Update vital signs
        if patient.vital_signs:
            self.vital_labels["Heart Rate"].text = f"{patient.vital_signs.pulse} BPM"
            self.vital_labels["Blood Pressure"].text = f"{patient.vital_signs.systolic_bp}/{patient.vital_signs.diastolic_bp} mmHg"
            self.vital_labels["Temperature"].text = f"{patient.vital_signs.temperature:.1f}°C"
            self.vital_labels["Respiratory Rate"].text = f"{patient.vital_signs.respiratory_rate} breaths/min"
            self.vital_labels["O₂ Saturation"].text = f"{patient.vital_signs.oxygen_saturation}%"
        
        # Update symptoms
        if patient.current_symptoms:
            self.symptoms_label.text = "• " + "\n• ".join(patient.current_symptoms)
        else:
            self.symptoms_label.text = "No symptoms reported"
    
    def get_condition_text(self, severity):
        if severity <= 3:
            return "Mild"
        elif severity <= 6:
            return "Moderate"
        elif severity <= 8:
            return "Serious"
        else:
            return "Critical"
    
    def show_tests(self, instance):
        if self.game_state.doctor and self.game_state.doctor.specialization:
            self.manager.get_screen('tests').update_tests()
            self.manager.current = 'tests'
    
    def show_treatments(self, instance):
        if self.game_state.doctor and self.game_state.doctor.specialization:
            self.manager.get_screen('treatments').update_treatments()
            self.manager.current = 'treatments'
    
    def show_medications(self, instance):
        if self.game_state.doctor and self.game_state.doctor.specialization:
            self.manager.get_screen('medications').update_for_patient()
            self.manager.current = 'medications'
    
    def show_diagnosis(self, instance):
        self.manager.get_screen('diagnosis').update_diagnoses()
        self.manager.current = 'diagnosis'
    
    def go_to_main(self, instance):
        self.manager.current = 'main_menu'
    
    def next_patient(self, instance):
        # Complete current case
        if self.game_state.current_patient:
            self.game_state.complete_current_case()
        
        # Load a new patient
        self.game_state.load_random_patient()
        self.update_patient_data()


class TestsScreen(Screen):
    def __init__(self, **kwargs):
        super(TestsScreen, self).__init__(**kwargs)
        self.game_state = App.get_running_app().game_state
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Add title
        title = Label(
            text="Available Tests",
            font_size=24,
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(title)
        
        # Create a scrollview for tests
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.tests_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.tests_layout.bind(minimum_height=self.tests_layout.setter('height'))
        scroll_view.add_widget(self.tests_layout)
        layout.add_widget(scroll_view)
        
        # Add button to return to patient view
        btn_back = Button(
            text="Back to Patient View",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_back.bind(on_press=self.go_to_patient)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def update_tests(self):
        self.tests_layout.clear_widgets()
        
        if not self.game_state.doctor or not self.game_state.doctor.specialization:
            label = Label(text="No specialization selected")
            self.tests_layout.add_widget(label)
            return
        
        available_tests = self.game_state.doctor.specialization.available_tests
        
        for test in available_tests:
            test_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
            
            test_label = Label(
                text=test,
                font_size=16,
                size_hint_x=0.7,
                halign='left',
                text_size=(Window.width * 0.7 - dp(20), dp(50))
            )
            test_box.add_widget(test_label)
            
            run_btn = Button(
                text="Run Test",
                size_hint_x=0.3,
                background_color=(0.2, 0.6, 0.8, 1)
            )
            run_btn.test_name = test
            run_btn.bind(on_press=self.run_test)
            test_box.add_widget(run_btn)
            
            self.tests_layout.add_widget(test_box)
    
    def run_test(self, instance):
        test_name = instance.test_name
        if self.game_state.current_patient:
            result = self.game_state.current_patient.perform_test(test_name)
            
            # Save test result
            if self.game_state.save_test_result:
                self.game_state.save_test_result(test_name, result)
                
            # Save test result to PostgreSQL database
            if test_name and result:
                # Serialize the result properly
                result_data = {
                    'values': result,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Save to database
                DBManager.save_test_result(
                    self.game_state.current_patient.patient_id,
                    test_name,
                    result_data
                )
                
                # If this is an imaging test, save the image record too
                if test_name in ['X-ray', 'ECG', 'MRI']:
                    # Generate a filename for the image
                    image_path = f"data/images/{test_name.lower()}_{self.game_state.current_patient.patient_id}.png"
                    
                    # Save image metadata to database
                    DBManager.save_imaging_result(
                        self.game_state.current_patient.patient_id,
                        test_name,
                        image_path,
                        f"Results from {test_name} test"
                    )
            
            # Show test results screen
            results_screen = self.manager.get_screen('test_results')
            results_screen.set_test_results(test_name, result)
            self.manager.current = 'test_results'
    
    def go_to_patient(self, instance):
        self.manager.current = 'patient'


class TestResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(TestResultsScreen, self).__init__(**kwargs)
        self.game_state = App.get_running_app().game_state
        self.result = None
        self.test_name = ""
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Add title
        self.title_label = Label(
            text="Test Results",
            font_size=24,
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(self.title_label)
        
        # Add scrollable content
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.results_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        scroll_view.add_widget(self.results_layout)
        layout.add_widget(scroll_view)
        
        # Add button to return to tests view
        btn_back = Button(
            text="Back to Tests",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_back.bind(on_press=self.go_to_tests)
        layout.add_widget(btn_back)
        
        # Add button to return to patient directly
        btn_patient = Button(
            text="Back to Patient",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.3, 0.3, 0.3, 1)
        )
        btn_patient.bind(on_press=self.go_to_patient)
        layout.add_widget(btn_patient)
        
        self.add_widget(layout)
    
    def set_test_results(self, test_name, result):
        self.test_name = test_name
        self.result = result
        self.title_label.text = f"Test Results: {test_name}"
        
        self.results_layout.clear_widgets()
        
        # Add message
        message_label = Label(
            text=result.get('message', ''),
            font_size=16,
            size_hint_y=None,
            height=dp(30),
            halign='center'
        )
        self.results_layout.add_widget(message_label)
        
        # Add details section
        if 'details' in result and result['details']:
            details_title = Label(
                text="Details",
                font_size=18,
                size_hint_y=None,
                height=dp(40),
                halign='left',
                text_size=(Window.width - dp(40), None)
            )
            self.results_layout.add_widget(details_title)
            
            # Check if there's an image path
            image_path = result['details'].get('image_path')
            
            if image_path and os.path.exists(image_path):
                # Add image
                img = Image(
                    source=image_path,
                    size_hint_y=None,
                    height=dp(300)
                )
                self.results_layout.add_widget(img)
            
            # Add other details
            for key, value in result['details'].items():
                if key != 'image_path':  # Skip image path, we've handled it
                    detail_box = BoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height=dp(30)
                    )
                    
                    key_label = Label(
                        text=key.replace('_', ' ').title() + ":",
                        font_size=14,
                        size_hint_x=0.4,
                        halign='right',
                        text_size=(Window.width * 0.4 - dp(10), dp(30))
                    )
                    detail_box.add_widget(key_label)
                    
                    value_label = Label(
                        text=str(value),
                        font_size=14,
                        size_hint_x=0.6,
                        halign='left',
                        text_size=(Window.width * 0.6 - dp(30), dp(30))
                    )
                    detail_box.add_widget(value_label)
                    
                    self.results_layout.add_widget(detail_box)
        
        # Add interpretation
        if 'interpretation' in result:
            interp_title = Label(
                text="Interpretation",
                font_size=18,
                size_hint_y=None,
                height=dp(40),
                halign='left',
                text_size=(Window.width - dp(40), None)
            )
            self.results_layout.add_widget(interp_title)
            
            interp_label = Label(
                text=result['interpretation'],
                font_size=14,
                size_hint_y=None,
                halign='left',
                text_size=(Window.width - dp(40), None)
            )
            interp_label.bind(texture_size=interp_label.setter('size'))
            self.results_layout.add_widget(interp_label)
        
        # Add abnormal flag if needed
        if result.get('is_abnormal', False):
            abnormal_label = Label(
                text="ABNORMAL FINDINGS DETECTED",
                font_size=16,
                size_hint_y=None,
                height=dp(40),
                color=(1, 0, 0, 1)
            )
            self.results_layout.add_widget(abnormal_label)
        
        # Add recommendations if any
        if 'recommendations' in result and result['recommendations']:
            rec_title = Label(
                text="Recommendations",
                font_size=18,
                size_hint_y=None,
                height=dp(40),
                halign='left',
                text_size=(Window.width - dp(40), None)
            )
            self.results_layout.add_widget(rec_title)
            
            for rec in result['recommendations']:
                rec_label = Label(
                    text=f"• {rec}",
                    font_size=14,
                    size_hint_y=None,
                    halign='left',
                    text_size=(Window.width - dp(40), None)
                )
                rec_label.bind(texture_size=rec_label.setter('size'))
                self.results_layout.add_widget(rec_label)
    
    def go_to_tests(self, instance):
        self.manager.current = 'tests'
    
    def go_to_patient(self, instance):
        self.manager.current = 'patient'


class TreatmentsScreen(Screen):
    def __init__(self, **kwargs):
        super(TreatmentsScreen, self).__init__(**kwargs)
        self.game_state = App.get_running_app().game_state
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Add title
        title = Label(
            text="Available Treatments",
            font_size=24,
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(title)
        
        # Create a scrollview for treatments
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.treatments_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.treatments_layout.bind(minimum_height=self.treatments_layout.setter('height'))
        scroll_view.add_widget(self.treatments_layout)
        layout.add_widget(scroll_view)
        
        # Add button to return to patient view
        btn_back = Button(
            text="Back to Patient View",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_back.bind(on_press=self.go_to_patient)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def update_treatments(self):
        self.treatments_layout.clear_widgets()
        
        if not self.game_state.doctor or not self.game_state.doctor.specialization:
            label = Label(text="No specialization selected")
            self.treatments_layout.add_widget(label)
            return
        
        available_treatments = self.game_state.doctor.specialization.available_treatments
        
        for treatment in available_treatments:
            treatment_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
            
            treatment_label = Label(
                text=treatment,
                font_size=16,
                size_hint_x=0.7,
                halign='left',
                text_size=(Window.width * 0.7 - dp(20), dp(50))
            )
            treatment_box.add_widget(treatment_label)
            
            apply_btn = Button(
                text="Apply",
                size_hint_x=0.3,
                background_color=(0.2, 0.8, 0.2, 1)
            )
            apply_btn.treatment_name = treatment
            apply_btn.bind(on_press=self.apply_treatment)
            treatment_box.add_widget(apply_btn)
            
            self.treatments_layout.add_widget(treatment_box)
    
    def apply_treatment(self, instance):
        treatment_name = instance.treatment_name
        if self.game_state.current_patient:
            result = self.game_state.current_patient.apply_treatment(treatment_name)
            
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
                    self.game_state.current_patient.patient_id,
                    treatment_name,
                    treatment_data
                )
                
                # Also update the patient record in the database
                DBManager.save_patient(self.game_state.current_patient)
            
            # Update patient screen
            self.manager.get_screen('patient').update_patient_data()
            
            # Show treatment results
            results_screen = self.manager.get_screen('treatment_results')
            results_screen.set_treatment_results(treatment_name, result)
            self.manager.current = 'treatment_results'
    
    def go_to_patient(self, instance):
        self.manager.current = 'patient'


class TreatmentResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(TreatmentResultsScreen, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Add title
        self.title_label = Label(
            text="Treatment Results",
            font_size=24,
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(self.title_label)
        
        # Add scrollable content
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.results_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        scroll_view.add_widget(self.results_layout)
        layout.add_widget(scroll_view)
        
        # Add buttons for navigation
        nav_buttons = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=10)
        
        btn_more = Button(
            text="Apply Another Treatment",
            size_hint_x=0.5,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        btn_more.bind(on_press=self.go_to_treatments)
        nav_buttons.add_widget(btn_more)
        
        btn_patient = Button(
            text="Back to Patient",
            size_hint_x=0.5,
            background_color=(0.3, 0.3, 0.3, 1)
        )
        btn_patient.bind(on_press=self.go_to_patient)
        nav_buttons.add_widget(btn_patient)
        
        layout.add_widget(nav_buttons)
        
        self.add_widget(layout)
    
    def set_treatment_results(self, treatment_name, result):
        self.title_label.text = f"Treatment Applied: {treatment_name}"
        
        self.results_layout.clear_widgets()
        
        # Add message
        message_label = Label(
            text=result.get('message', ''),
            font_size=16,
            size_hint_y=None,
            height=dp(40),
            halign='center'
        )
        self.results_layout.add_widget(message_label)
        
        # Add effects if any
        if 'effects' in result and result['effects']:
            effects_title = Label(
                text="Effects",
                font_size=18,
                size_hint_y=None,
                height=dp(40)
            )
            self.results_layout.add_widget(effects_title)
            
            for effect in result['effects']:
                effect_label = Label(
                    text=f"• {effect}",
                    font_size=14,
                    size_hint_y=None,
                    halign='left',
                    text_size=(Window.width - dp(40), None)
                )
                effect_label.bind(texture_size=effect_label.setter('size'))
                self.results_layout.add_widget(effect_label)
        
        # Add vital changes if any
        if 'vital_changes' in result and result['vital_changes']:
            vitals_title = Label(
                text="Vital Sign Changes",
                font_size=18,
                size_hint_y=None,
                height=dp(40)
            )
            self.results_layout.add_widget(vitals_title)
            
            for vital, change in result['vital_changes'].items():
                vital_label = Label(
                    text=f"• {vital.replace('_', ' ').title()}: {change}",
                    font_size=14,
                    size_hint_y=None,
                    halign='left',
                    text_size=(Window.width - dp(40), None)
                )
                vital_label.bind(texture_size=vital_label.setter('size'))
                self.results_layout.add_widget(vital_label)
    
    def go_to_treatments(self, instance):
        self.manager.current = 'treatments'
    
    def go_to_patient(self, instance):
        self.manager.current = 'patient'


class DiagnosisScreen(Screen):
    def __init__(self, **kwargs):
        super(DiagnosisScreen, self).__init__(**kwargs)
        self.game_state = App.get_running_app().game_state
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Add title
        title = Label(
            text="Make Diagnosis",
            font_size=24,
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(title)
        
        # Add instructions
        instructions = Label(
            text="Based on the patient's symptoms and test results, select the most likely diagnosis:",
            font_size=14,
            size_hint_y=None,
            height=dp(30),
            halign='left',
            text_size=(Window.width - dp(40), None)
        )
        layout.add_widget(instructions)
        
        # Create a scrollview for diagnoses
        scroll_view = ScrollView(size_hint=(1, 0.7))
        self.diagnoses_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.diagnoses_layout.bind(minimum_height=self.diagnoses_layout.setter('height'))
        scroll_view.add_widget(self.diagnoses_layout)
        layout.add_widget(scroll_view)
        
        # Add button to return to patient view
        btn_back = Button(
            text="Back to Patient View",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_back.bind(on_press=self.go_to_patient)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def update_diagnoses(self):
        self.diagnoses_layout.clear_widgets()
        
        if not self.game_state.current_patient:
            label = Label(text="No patient loaded")
            self.diagnoses_layout.add_widget(label)
            return
        
        patient = self.game_state.current_patient
        
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
        non_matched = [d for d in all_diagnoses if d.name not in matched_names]
        non_matched.sort(key=lambda x: x.name)
        
        # First show matched diagnoses with confidence levels
        if diagnostic_matches:
            matched_label = Label(
                text="Recommended Diagnoses (based on symptoms and tests)",
                font_size=16,
                size_hint_y=None,
                height=dp(30),
                color=(0.2, 0.7, 0.2, 1)
            )
            self.diagnoses_layout.add_widget(matched_label)
            
            for diagnosis, confidence in diagnostic_matches:
                confidence_pct = int(confidence * 100)
                diag_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(70))
                
                diag_info = BoxLayout(orientation='vertical', size_hint_x=0.7)
                diag_name = Label(
                    text=diagnosis.name,
                    font_size=16,
                    halign='left',
                    size_hint_y=0.6,
                    text_size=(Window.width * 0.7 - dp(20), None)
                )
                diag_info.add_widget(diag_name)
                
                diag_conf = Label(
                    text=f"Confidence: {confidence_pct}%",
                    font_size=14,
                    halign='left',
                    size_hint_y=0.4,
                    text_size=(Window.width * 0.7 - dp(20), None),
                    color=(0.2, 0.7, 0.2, 1) if confidence > 0.5 else (0.7, 0.7, 0.2, 1)
                )
                diag_info.add_widget(diag_conf)
                
                diag_box.add_widget(diag_info)
                
                select_btn = Button(
                    text="Select",
                    size_hint_x=0.3,
                    background_color=(0.2, 0.6, 0.8, 1)
                )
                select_btn.diagnosis = diagnosis
                select_btn.confidence = confidence
                select_btn.bind(on_press=self.make_diagnosis)
                diag_box.add_widget(select_btn)
                
                self.diagnoses_layout.add_widget(diag_box)
        
        # Then show other possible diagnoses
        if non_matched:
            other_label = Label(
                text="Other Possible Diagnoses",
                font_size=16,
                size_hint_y=None,
                height=dp(30),
                color=(0.5, 0.5, 0.5, 1)
            )
            self.diagnoses_layout.add_widget(other_label)
            
            for diagnosis in non_matched:
                diag_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
                
                diag_name = Label(
                    text=diagnosis.name,
                    font_size=16,
                    halign='left',
                    size_hint_x=0.7,
                    text_size=(Window.width * 0.7 - dp(20), dp(50))
                )
                diag_box.add_widget(diag_name)
                
                select_btn = Button(
                    text="Select",
                    size_hint_x=0.3,
                    background_color=(0.5, 0.5, 0.5, 1)
                )
                select_btn.diagnosis = diagnosis
                select_btn.confidence = 0.0
                select_btn.bind(on_press=self.make_diagnosis)
                diag_box.add_widget(select_btn)
                
                self.diagnoses_layout.add_widget(diag_box)
    
    def make_diagnosis(self, instance):
        diagnosis = instance.diagnosis
        confidence = instance.confidence
        
        if self.game_state.current_patient:
            # Check if diagnosis is correct
            is_correct = confidence > 0.6
            if instance.confidence == 0 and len(self.game_state.current_patient.current_symptoms) == 0:
                # If no symptoms and chose "No significant findings", that's correct
                if diagnosis.name == "No Significant Findings":
                    is_correct = True
            
            # Update doctor's statistics
            if self.game_state.doctor:
                self.game_state.doctor.diagnose_patient(is_correct)
                # Save doctor data to PostgreSQL database
                DBManager.save_doctor(self.game_state.doctor)
            
            # Set the diagnosis on the patient
            self.game_state.current_patient.diagnosis = diagnosis.name
            
            # Update patient condition
            if is_correct:
                # Improve patient condition due to correct diagnosis
                self.game_state.current_patient.update_condition(-2)
            else:
                # Worsen patient condition slightly due to incorrect diagnosis
                self.game_state.current_patient.update_condition(1)
                
            # Save patient data to PostgreSQL database
            DBManager.save_patient(self.game_state.current_patient)
            
            # Record the diagnosis in the database
            diagnosis_result = {
                'diagnosis_name': diagnosis.name,
                'is_correct': is_correct,
                'confidence': confidence * 100,  # Convert to percentage
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Save the diagnosis result as a special type of test result
            DBManager.save_test_result(
                self.game_state.current_patient.patient_id, 
                "Final_Diagnosis", 
                diagnosis_result
            )
            
            # Show diagnosis results
            results_screen = self.manager.get_screen('diagnosis_results')
            results_screen.set_diagnosis_results(diagnosis, is_correct)
            self.manager.current = 'diagnosis_results'
    
    def go_to_patient(self, instance):
        self.manager.current = 'patient'


class DiagnosisResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(DiagnosisResultsScreen, self).__init__(**kwargs)
        self.game_state = App.get_running_app().game_state
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        # Add title
        self.title_label = Label(
            text="Diagnosis Made",
            font_size=24,
            size_hint_y=None,
            height=dp(40)
        )
        layout.add_widget(self.title_label)
        
        # Add scrollable content
        scroll_view = ScrollView(size_hint=(1, 0.8))
        self.results_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        scroll_view.add_widget(self.results_layout)
        layout.add_widget(scroll_view)
        
        # Add buttons for navigation
        btn_patient = Button(
            text="Back to Patient",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_patient.bind(on_press=self.go_to_patient)
        layout.add_widget(btn_patient)
        
        btn_next = Button(
            text="Next Patient",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.8, 0.2, 1)
        )
        btn_next.bind(on_press=self.next_patient)
        layout.add_widget(btn_next)
        
        self.add_widget(layout)
    
    def set_diagnosis_results(self, diagnosis, is_correct):
        self.title_label.text = f"Diagnosis Made: {diagnosis.name}"
        
        self.results_layout.clear_widgets()
        
        # Add description
        desc_box = BoxLayout(orientation='vertical', size_hint_y=None, padding=(0, 10))
        desc_label = Label(
            text=diagnosis.description,
            font_size=14,
            halign='left',
            text_size=(Window.width - dp(40), None)
        )
        desc_label.bind(texture_size=desc_label.setter('size'))
        desc_box.add_widget(desc_label)
        desc_box.height = desc_label.height + dp(20)
        self.results_layout.add_widget(desc_box)
        
        # Add correctness feedback
        if is_correct:
            correct_label = Label(
                text="Your diagnosis appears to be accurate based on the patient's symptoms and test results.",
                font_size=16,
                size_hint_y=None,
                halign='left',
                text_size=(Window.width - dp(40), None),
                color=(0.2, 0.8, 0.2, 1)
            )
            correct_label.bind(texture_size=correct_label.setter('size'))
            self.results_layout.add_widget(correct_label)
        else:
            incorrect_label = Label(
                text="Your diagnosis may not fully align with the patient's symptoms and test results.",
                font_size=16,
                size_hint_y=None,
                halign='left',
                text_size=(Window.width - dp(40), None),
                color=(0.8, 0.2, 0.2, 1)
            )
            incorrect_label.bind(texture_size=incorrect_label.setter('size'))
            self.results_layout.add_widget(incorrect_label)
        
        # Add recommended actions section
        actions_title = Label(
            text="Recommended Actions",
            font_size=18,
            size_hint_y=None,
            height=dp(40),
            halign='left',
            text_size=(Window.width - dp(40), None)
        )
        self.results_layout.add_widget(actions_title)
        
        # Add recommended tests
        if diagnosis.recommended_tests:
            tests_title = Label(
                text="Recommended tests:",
                font_size=14,
                size_hint_y=None,
                height=dp(30),
                halign='left',
                text_size=(Window.width - dp(40), None)
            )
            self.results_layout.add_widget(tests_title)
            
            # Get list of performed tests
            performed_tests = []
            if self.game_state.current_patient:
                performed_tests = [test['test'] for test in self.game_state.current_patient.tests_performed]
            
            for test in diagnosis.recommended_tests:
                status = "✓" if test in performed_tests else "□"
                test_label = Label(
                    text=f"{status} {test}",
                    font_size=14,
                    size_hint_y=None,
                    height=dp(20),
                    halign='left',
                    text_size=(Window.width - dp(40), None)
                )
                self.results_layout.add_widget(test_label)
        
        # Add recommended treatments
        if diagnosis.recommended_treatments:
            treatments_title = Label(
                text="Recommended treatments:",
                font_size=14,
                size_hint_y=None,
                height=dp(30),
                halign='left',
                text_size=(Window.width - dp(40), None)
            )
            self.results_layout.add_widget(treatments_title)
            
            for treatment in diagnosis.recommended_treatments:
                treatment_label = Label(
                    text=f"• {treatment}",
                    font_size=14,
                    size_hint_y=None,
                    height=dp(20),
                    halign='left',
                    text_size=(Window.width - dp(40), None)
                )
                self.results_layout.add_widget(treatment_label)
        
        # Add score information
        if self.game_state.doctor:
            score_label = Label(
                text=f"Current score: {self.game_state.doctor.score}",
                font_size=16,
                size_hint_y=None,
                height=dp(40),
                halign='center'
            )
            self.results_layout.add_widget(score_label)
    
    def go_to_patient(self, instance):
        self.manager.current = 'patient'
    
    def next_patient(self, instance):
        # Complete current case
        if self.game_state.current_patient:
            self.game_state.complete_current_case()
        
        # Load a new patient
        self.game_state.load_random_patient()
        self.manager.get_screen('patient').update_patient_data()
        self.manager.current = 'patient'


class VirtualDoctorApp(App):
    def build(self):
        # Initialize the database if needed
        print("Initializing PostgreSQL database...")
        # Initialize database tables if they don't exist
        
        # Create the game state
        self.game_state = GameState()
        
        # Initialize user variable for authentication
        self.current_user = None
        
        # Initialize medical conditions in the database
        print("Loading medical conditions into database...")
        DBManager.initialize_conditions()
        
        # Create the screen manager
        sm = ScreenManager()
        
        # Add all game screens
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(AboutScreen(name='about'))
        sm.add_widget(SpecializationScreen(name='specialization'))
        sm.add_widget(PatientScreen(name='patient'))
        sm.add_widget(TestsScreen(name='tests'))
        sm.add_widget(TestResultsScreen(name='test_results'))
        sm.add_widget(TreatmentsScreen(name='treatments'))
        sm.add_widget(TreatmentResultsScreen(name='treatment_results'))
        sm.add_widget(DiagnosisScreen(name='diagnosis'))
        sm.add_widget(DiagnosisResultsScreen(name='diagnosis_results'))
        
        # Import user screens
        from screens.login_screen import LoginScreen
        from screens.register_screen import RegisterScreen
        from screens.dashboard_screen import DashboardScreen
        
        # Add user management screens
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        
        print("VirtualDoctor app initialized with PostgreSQL database")
        return sm


if __name__ == '__main__':
    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # If logo doesn't exist, create a simple placeholder
    if not os.path.exists('assets/logo.png'):
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Generate a simple caduceus symbol
        plt.figure(figsize=(5, 5))
        plt.axis('off')
        
        # Draw circle
        circle = plt.Circle((0.5, 0.5), 0.4, fill=False, color='blue', linewidth=2)
        plt.gca().add_patch(circle)
        
        # Draw staff
        plt.plot([0.5, 0.5], [0.1, 0.9], 'b-', linewidth=3)
        
        # Draw snakes
        t = np.linspace(0, 1, 100)
        snake1_x = 0.5 + 0.1 * np.sin(2 * np.pi * 3 * t)
        snake1_y = 0.1 + 0.8 * t
        plt.plot(snake1_x, snake1_y, 'g-', linewidth=2)
        
        snake2_x = 0.5 - 0.1 * np.sin(2 * np.pi * 3 * t)
        snake2_y = 0.1 + 0.8 * t
        plt.plot(snake2_x, snake2_y, 'g-', linewidth=2)
        
        plt.title("VirtualDoctor", fontsize=20)
        # plt.savefig('assets/logo.png', bbox_inches='tight', dpi=100)
        plt.savefig('generated-icon.png', bbox_inches='tight', dpi=100)
        plt.close()
    
    VirtualDoctorApp().run()