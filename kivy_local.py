"""
VirtualDoctor - Kivy GUI Version (Local SQLite version)
A medical simulation game with graphical interface
"""
import os
import sys
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp

# Make sure local modules can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our screens and game state
from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.dashboard_screen import DashboardScreen
from screens.medications_screen import MedicationsScreen
from screens.test_screens import TestsScreen, TestResultsScreen
from screens.treatment_screens import TreatmentsScreen, TreatmentResultsScreen
from screens.diagnosis_screens import DiagnosisScreen, DiagnosisResultsScreen
from utils.game_state import GameState

# Import the local database
from utils.local_db import init_db, engine, Session
from models.database_models import Base

# Initialize the local database
init_db()

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        self.name = 'main_menu'
        
        # Create a layout with a background color
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with self.layout.canvas.before:
            Color(0.1, 0.1, 0.3, 1)  # Dark blue background
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)
        
        # Add a title
        self.title = Label(
            text='VirtualDoctor',
            font_size=36,
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(self.title)
        
        # Add a subtitle
        self.subtitle = Label(
            text='Medical Simulation',
            font_size=18,
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.subtitle)
        
        # Button layout
        self.button_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(1, 0.5),
            padding=[50, 10, 50, 10]
        )
        
        # Start Game button
        self.start_btn = Button(
            text='Start Game',
            size_hint=(1, 0.25),
            background_color=(0.2, 0.7, 0.3, 1)  # Green
        )
        self.start_btn.bind(on_release=self.go_to_specialization)
        self.button_layout.add_widget(self.start_btn)
        
        # Login button
        self.login_btn = Button(
            text='Login',
            size_hint=(1, 0.25),
            background_color=(0.3, 0.5, 0.9, 1)  # Blue
        )
        self.login_btn.bind(on_release=self.go_to_login)
        self.button_layout.add_widget(self.login_btn)
        
        # About button
        self.about_btn = Button(
            text='About',
            size_hint=(1, 0.25),
            background_color=(0.7, 0.7, 0.7, 1)  # Gray
        )
        self.about_btn.bind(on_release=self.go_to_about)
        self.button_layout.add_widget(self.about_btn)
        
        # Quit button
        self.quit_btn = Button(
            text='Quit',
            size_hint=(1, 0.25),
            background_color=(0.9, 0.3, 0.3, 1)  # Red
        )
        self.quit_btn.bind(on_release=self.quit_app)
        self.button_layout.add_widget(self.quit_btn)
        
        self.layout.add_widget(self.button_layout)
        
        # User info at the bottom
        self.user_info = Label(
            text='Not logged in',
            font_size=14,
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.user_info)
        
        self.add_widget(self.layout)
        
    def update_rect(self, instance, value):
        """Update rectangle position and size"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def go_to_specialization(self, instance):
        """Go to specialization selection screen"""
        app = App.get_running_app()
        
        if app.current_user:
            # If user is logged in, load their data
            app.game_state.set_current_user(app.current_user)
            self.manager.get_screen('specialization').reset()
            self.manager.transition.direction = 'left'
            self.manager.current = 'specialization'
        else:
            # Start without login
            app.game_state.reset_game()
            self.manager.get_screen('specialization').reset()
            self.manager.transition.direction = 'left'
            self.manager.current = 'specialization'
    
    def go_to_login(self, instance):
        """Go to login screen"""
        self.manager.transition.direction = 'left'
        self.manager.current = 'login'
    
    def go_to_about(self, instance):
        """Go to about screen"""
        self.manager.transition.direction = 'left'
        self.manager.current = 'about'
    
    def quit_app(self, instance):
        """Quit the application"""
        App.get_running_app().stop()
    
    def update_for_logged_user(self, user):
        """Update the UI when a user is logged in"""
        if user:
            #how it was:
            #self.user_info.text = f'Logged in as: {user.username}'

            #proposed fix:
            self.user_info.text = f'Logged in as: {user["username"]}'
            self.login_btn.text = 'Dashboard'
            self.login_btn.background_color = (0.3, 0.7, 0.5, 1)  # Teal
            self.login_btn.unbind(on_release=self.go_to_login)
            self.login_btn.bind(on_release=self.go_to_dashboard)
        else:
            self.user_info.text = 'Not logged in'
            self.login_btn.text = 'Login'
            self.login_btn.background_color = (0.3, 0.5, 0.9, 1)  # Blue
            self.login_btn.unbind(on_release=self.go_to_dashboard)
            self.login_btn.bind(on_release=self.go_to_login)
    
    def go_to_dashboard(self, instance):
        """Go to user dashboard"""
        self.manager.transition.direction = 'left'
        self.manager.current = 'dashboard'


class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)
        self.name = 'about'
        
        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with self.layout.canvas.before:
            Color(0.1, 0.1, 0.3, 1)  # Dark blue background
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)
        
        # Add a title
        self.title = Label(
            text='About VirtualDoctor',
            font_size=30,
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(self.title)
        
        # Description text
        self.description = Label(
            text='VirtualDoctor is a medical simulation game where you can practice diagnosis and treatment in a virtual environment.\n\n'
                 'Features:\n'
                 '- Multiple medical specializations\n'
                 '- Realistic patient symptoms and conditions\n'
                 '- Various medical tests and procedures\n'
                 '- Medication administration system with patient responses\n'
                 '- Experience points and progression system\n\n'
                 'Version: 1.0.0 (SQLite Local Edition)',
            font_size=16,
            halign='left',
            valign='top',
            size_hint=(1, 0.7)
        )
        self.description.bind(size=self.description.setter('text_size'))
        self.layout.add_widget(self.description)
        
        # Back button
        self.back_btn = Button(
            text='Back to Main Menu',
            size_hint=(1, 0.1),
            background_color=(0.3, 0.5, 0.9, 1)  # Blue
        )
        self.back_btn.bind(on_release=self.go_to_main)
        self.layout.add_widget(self.back_btn)
        
        self.add_widget(self.layout)
    
    def update_rect(self, instance, value):
        """Update rectangle position and size"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def go_to_main(self, instance):
        """Go back to main menu"""
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_menu'

from kivy_doctor import VirtualDoctorApp

class SpecializationScreen(Screen):
    def __init__(self, **kwargs):
        super(SpecializationScreen, self).__init__(**kwargs)
        self.name = 'specialization'
        self.game_state = App.get_running_app().game_state
        
        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with self.layout.canvas.before:
            Color(0.1, 0.1, 0.3, 1)  # Dark blue background
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self.update_rect, pos=self.update_rect)
        
        # Title
        self.title = Label(
            text='Select Your Specialization',
            font_size=30,
            size_hint=(1, 0.2)
        )
        self.layout.add_widget(self.title)
        
        # Specialization grid
        self.specialization_grid = GridLayout(
            cols=2,
            spacing=10,
            padding=10,
            size_hint=(1, 0.7)
        )
        self.layout.add_widget(self.specialization_grid)
        
        # Back button
        self.back_btn = Button(
            text='Back to Main Menu',
            size_hint=(1, 0.1),
            background_color=(0.3, 0.5, 0.9, 1)  # Blue
        )
        self.back_btn.bind(on_release=self.go_to_main)
        self.layout.add_widget(self.back_btn)
        
        self.add_widget(self.layout)
        
        # Populate specializations
        self.populate_specializations()
    
    def update_rect(self, instance, value):
        """Update rectangle position and size"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def populate_specializations(self):
        """Populate the specialization grid with buttons"""
        # Clear existing buttons
        self.specialization_grid.clear_widgets()
        
        # Add specialization buttons
        specializations = [
            {'name': 'Cardiology', 'description': 'Heart and circulatory system'},
            {'name': 'Neurology', 'description': 'Brain and nervous system'},
            {'name': 'Pulmonology', 'description': 'Lungs and respiratory system'},
            {'name': 'Gastroenterology', 'description': 'Digestive system'},
            {'name': 'Orthopedics', 'description': 'Bones and joints'},
            {'name': 'Emergency Medicine', 'description': 'Acute care'}
        ]
        
        for spec in specializations:
            # Create a box for each specialization
            box = BoxLayout(orientation='vertical')
            
            # Specialization button
            btn = Button(
                text=spec['name'],
                size_hint=(1, 0.7),
                background_color=(0.2, 0.6, 0.8, 1)
            )
            btn.specialization = spec['name']
            btn.bind(on_release=self.select_specialization)
            box.add_widget(btn)
            
            # Description label
            lbl = Label(
                text=spec['description'],
                size_hint=(1, 0.3)
            )
            box.add_widget(lbl)
            
            self.specialization_grid.add_widget(box)
    
    def select_specialization(self, instance):
        """Select a specialization and move to patient screen"""
        # Set the specialization in the game state
        if self.game_state:
            self.game_state.set_doctor_specialization(instance.specialization)
            
            # Load a patient
            self.game_state.load_random_patient()
            
            # Go to patient screen
            self.manager.transition.direction = 'left'
            self.manager.current = 'patient'
            self.manager.get_screen('patient').update_patient_data()
    
    def go_to_main(self, instance):
        """Go back to main menu"""
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_menu'
    
    def reset(self):
        """Reset the specialization screen"""
        self.populate_specializations()


class PatientScreen(Screen):
    def __init__(self, **kwargs):
        super(PatientScreen, self).__init__(**kwargs)
        self.name = 'patient'
        self.game_state = App.get_running_app().game_state
        
        # Main layout
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
        
        # Create labels for vital signs
        vital_signs = ["Heart Rate", "Blood Pressure", "Temperature", "Respiratory Rate", "O2 Saturation"]
        self.vital_labels = {}
        
        for vital in vital_signs:
            name_label = Label(text=vital, halign='left', font_size=14)
            value_label = Label(text="--", halign='left', font_size=14)
            vitals_grid.add_widget(name_label)
            vitals_grid.add_widget(value_label)
            self.vital_labels[vital] = value_label
        
        vitals_panel.add_widget(vitals_grid)
        top_panel.add_widget(vitals_panel)
        
        layout.add_widget(top_panel)
        
        # Middle panel with symptoms
        middle_panel = BoxLayout(orientation='vertical', size_hint_y=0.2)
        symptoms_label_title = Label(text="Current Symptoms", font_size=18, size_hint_y=0.3)
        middle_panel.add_widget(symptoms_label_title)
        
        self.symptoms_label = Label(text="", halign='left', valign='top', font_size=14, size_hint_y=0.7)
        self.symptoms_label.bind(size=self.symptoms_label.setter('text_size'))
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
            self.vital_labels["O2 Saturation"].text = f"{patient.vital_signs.oxygen_saturation}%"
        
        # Update symptoms
        if patient.current_symptoms:
            self.symptoms_label.text = ", ".join(patient.current_symptoms)
        else:
            self.symptoms_label.text = "No visible symptoms"
    
    def get_condition_text(self, severity):
        if severity == 1:
            return "Stable"
        elif severity == 2:
            return "Fair"
        elif severity == 3:
            return "Serious"
        elif severity == 4:
            return "Critical"
        else:
            return "Unknown"
    
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
        
        # Update UI
        self.update_patient_data()


class VirtualDoctorApp(App):
    def __init__(self, **kwargs):
        super(VirtualDoctorApp, self).__init__(**kwargs)
        self.game_state = GameState()
        self.current_user = None

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        
        # Add all screens with explicit names
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
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(MedicationsScreen(name='medications'))
        
        return sm


if __name__ == '__main__':
    VirtualDoctorApp().run()