from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.popup import Popup
from kivy.clock import Clock
import random

from utils.game_state import GameState
from models.patient import Patient

class VitalsMonitor(BoxLayout):
    """Widget for displaying patient vital signs in a monitor-like interface."""
    
    def __init__(self, patient: Patient, **kwargs):
        super(VitalsMonitor, self).__init__(**kwargs)
        self.patient = patient
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(200)
        
        # Add a border and background to the monitor
        with self.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Dark background
            self.rect = Rectangle(pos=self.pos, size=self.size)
            Color(0, 0.8, 0, 1)  # Green grid lines
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Title label
        title = Label(
            text="PATIENT VITALS",
            font_size=dp(18),
            bold=True,
            color=(0, 0.8, 0, 1),  # Green text
            size_hint_y=0.2
        )
        self.add_widget(title)
        
        # Grid for vitals
        vitals_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.8)
        
        # Add vital signs
        vitals = self.patient.vital_signs.get_vitals_dict()
        
        # Heart rate
        vitals_grid.add_widget(Label(
            text="Heart Rate:",
            color=(0.8, 0.8, 0.8, 1),  # Light gray
            halign='right',
            size_hint_x=0.4
        ))
        self.pulse_label = Label(
            text=f"{self.patient.vital_signs.pulse} BPM",
            color=(1, 0.5, 0.5, 1),  # Light red
            halign='left',
            size_hint_x=0.6
        )
        vitals_grid.add_widget(self.pulse_label)
        
        # Blood pressure
        vitals_grid.add_widget(Label(
            text="Blood Pressure:",
            color=(0.8, 0.8, 0.8, 1),
            halign='right',
            size_hint_x=0.4
        ))
        self.bp_label = Label(
            text=vitals['blood_pressure'],
            color=(0.5, 0.8, 1, 1),  # Light blue
            halign='left',
            size_hint_x=0.6
        )
        vitals_grid.add_widget(self.bp_label)
        
        # Temperature
        vitals_grid.add_widget(Label(
            text="Temperature:",
            color=(0.8, 0.8, 0.8, 1),
            halign='right',
            size_hint_x=0.4
        ))
        self.temp_label = Label(
            text=vitals['temperature'],
            color=(1, 0.8, 0.5, 1),  # Light orange
            halign='left',
            size_hint_x=0.6
        )
        vitals_grid.add_widget(self.temp_label)
        
        # Respiratory rate
        vitals_grid.add_widget(Label(
            text="Resp. Rate:",
            color=(0.8, 0.8, 0.8, 1),
            halign='right',
            size_hint_x=0.4
        ))
        self.resp_label = Label(
            text=f"{self.patient.vital_signs.respiratory_rate} breaths/min",
            color=(0.5, 1, 0.5, 1),  # Light green
            halign='left',
            size_hint_x=0.6
        )
        vitals_grid.add_widget(self.resp_label)
        
        # Oxygen saturation
        vitals_grid.add_widget(Label(
            text="O₂ Saturation:",
            color=(0.8, 0.8, 0.8, 1),
            halign='right',
            size_hint_x=0.4
        ))
        self.o2_label = Label(
            text=vitals['oxygen_saturation'],
            color=(0.8, 0.8, 1, 1),  # Light purple
            halign='left',
            size_hint_x=0.6
        )
        vitals_grid.add_widget(self.o2_label)
        
        self.add_widget(vitals_grid)
        
        # Start the vitals update clock
        Clock.schedule_interval(self.update_vitals, 2.0)  # Update every 2 seconds
    
    def update_rect(self, *args):
        """Update rectangle position and size when widget position or size changes."""
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def update_vitals(self, dt):
        """
        Update vital signs display with small random fluctuations to simulate real-time monitoring.
        
        Args:
            dt: Time delta from scheduler
        """
        # Update pulse with small random fluctuation
        pulse_change = random.randint(-2, 2)
        new_pulse = max(40, min(180, self.patient.vital_signs.pulse + pulse_change))
        self.patient.vital_signs.pulse = new_pulse
        self.pulse_label.text = f"{new_pulse} BPM"
        
        # Update blood pressure
        sys_change = random.randint(-2, 2)
        dia_change = random.randint(-1, 1)
        new_sys = max(80, min(200, self.patient.vital_signs.systolic_bp + sys_change))
        new_dia = max(40, min(120, self.patient.vital_signs.diastolic_bp + dia_change))
        self.patient.vital_signs.systolic_bp = new_sys
        self.patient.vital_signs.diastolic_bp = new_dia
        self.bp_label.text = f"{new_sys}/{new_dia} mmHg"
        
        # Update temperature with tiny fluctuation
        temp_change = random.uniform(-0.1, 0.1)
        new_temp = max(35.0, min(41.0, self.patient.vital_signs.temperature + temp_change))
        self.patient.vital_signs.temperature = new_temp
        self.temp_label.text = f"{new_temp:.1f}°C"
        
        # Update respiratory rate
        resp_change = random.randint(-1, 1)
        new_resp = max(8, min(30, self.patient.vital_signs.respiratory_rate + resp_change))
        self.patient.vital_signs.respiratory_rate = new_resp
        self.resp_label.text = f"{new_resp} breaths/min"
        
        # Update oxygen saturation
        o2_change = random.randint(-1, 1)
        new_o2 = max(70, min(100, self.patient.vital_signs.oxygen_saturation + o2_change))
        self.patient.vital_signs.oxygen_saturation = new_o2
        self.o2_label.text = f"{new_o2}%"
        
        # Change color based on patient condition
        if self.patient.is_critical():
            self.pulse_label.color = (1, 0, 0, 1)  # Bright red for critical
            Clock.schedule_once(lambda dt: self.pulse_label.setter('color')((1, 0.5, 0.5, 1)), 0.5)  # Blink
        else:
            self.pulse_label.color = (1, 0.5, 0.5, 1)  # Normal light red


class PatientInfoPanel(BoxLayout):
    """Widget displaying basic patient information."""
    
    def __init__(self, patient: Patient, **kwargs):
        super(PatientInfoPanel, self).__init__(**kwargs)
        self.patient = patient
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(150)
        
        # Add a border and background
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)  # Dark background
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Patient info header
        header = Label(
            text="PATIENT INFORMATION",
            font_size=dp(16),
            bold=True,
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=0.2
        )
        self.add_widget(header)
        
        # Patient details grid
        info_grid = GridLayout(cols=2, spacing=dp(5), size_hint_y=0.8)
        
        # Name
        info_grid.add_widget(Label(
            text="Name:",
            halign='right',
            size_hint_x=0.3,
            color=(0.7, 0.7, 0.7, 1)
        ))
        info_grid.add_widget(Label(
            text=patient.name,
            halign='left',
            size_hint_x=0.7,
            color=(1, 1, 1, 1)
        ))
        
        # Age and Gender
        info_grid.add_widget(Label(
            text="Age/Gender:",
            halign='right',
            size_hint_x=0.3,
            color=(0.7, 0.7, 0.7, 1)
        ))
        info_grid.add_widget(Label(
            text=f"{patient.age} years, {patient.gender}",
            halign='left',
            size_hint_x=0.7,
            color=(1, 1, 1, 1)
        ))
        
        # Medical History
        info_grid.add_widget(Label(
            text="History:",
            halign='right',
            valign='top',
            size_hint_x=0.3,
            color=(0.7, 0.7, 0.7, 1)
        ))
        history_text = ", ".join(patient.medical_history) if patient.medical_history else "No significant history"
        info_grid.add_widget(Label(
            text=history_text,
            halign='left',
            text_size=(dp(300), None),
            size_hint_x=0.7,
            color=(1, 1, 1, 1)
        ))
        
        # Current condition severity
        info_grid.add_widget(Label(
            text="Condition:",
            halign='right',
            size_hint_x=0.3,
            color=(0.7, 0.7, 0.7, 1)
        ))
        
        # Determine condition text based on severity
        condition_text = "Stable"
        condition_color = (0.2, 0.8, 0.2, 1)  # Green
        
        if patient.condition_severity >= 8:
            condition_text = "Critical"
            condition_color = (0.9, 0.1, 0.1, 1)  # Red
        elif patient.condition_severity >= 5:
            condition_text = "Serious"
            condition_color = (0.9, 0.6, 0.1, 1)  # Orange
        elif patient.condition_severity >= 3:
            condition_text = "Fair"
            condition_color = (0.9, 0.9, 0.1, 1)  # Yellow
            
        condition_label = Label(
            text=condition_text,
            halign='left',
            size_hint_x=0.7,
            color=condition_color
        )
        info_grid.add_widget(condition_label)
        
        self.add_widget(info_grid)
    
    def update_rect(self, *args):
        """Update rectangle position and size when widget position or size changes."""
        self.rect.pos = self.pos
        self.rect.size = self.size


class SymptomsPanel(BoxLayout):
    """Widget displaying patient symptoms."""
    
    def __init__(self, patient: Patient, **kwargs):
        super(SymptomsPanel, self).__init__(**kwargs)
        self.patient = patient
        self.orientation = 'vertical'
        self.padding = dp(10)
        self.spacing = dp(5)
        
        # Add a border and background
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)  # Dark background
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Symptoms header
        header = Label(
            text="PATIENT SYMPTOMS",
            font_size=dp(16),
            bold=True,
            color=(0.9, 0.9, 0.9, 1),
            size_hint_y=0.1
        )
        self.add_widget(header)
        
        # Scrollable symptom list
        scroll_view = ScrollView(size_hint=(1, 0.9))
        self.symptom_list = GridLayout(cols=1, spacing=dp(5), size_hint_y=None)
        self.symptom_list.bind(minimum_height=self.symptom_list.setter('height'))
        
        # Add symptoms
        if patient.current_symptoms:
            for symptom in patient.current_symptoms:
                symptom_item = Label(
                    text=f"• {symptom}",
                    halign='left',
                    valign='middle',
                    size_hint_y=None,
                    height=dp(30),
                    text_size=(dp(300), dp(30)),
                    color=(1, 0.8, 0.8, 1)  # Light red for symptoms
                )
                self.symptom_list.add_widget(symptom_item)
        else:
            no_symptoms = Label(
                text="No reported symptoms",
                halign='center',
                valign='middle',
                size_hint_y=None,
                height=dp(30),
                color=(0.7, 0.7, 0.7, 1)
            )
            self.symptom_list.add_widget(no_symptoms)
        
        scroll_view.add_widget(self.symptom_list)
        self.add_widget(scroll_view)
    
    def update_rect(self, *args):
        """Update rectangle position and size when widget position or size changes."""
        self.rect.pos = self.pos
        self.rect.size = self.size


class ActionPanel(BoxLayout):
    """Widget containing action buttons for patient interaction."""
    
    def __init__(self, callback_handler, **kwargs):
        super(ActionPanel, self).__init__(**kwargs)
        self.callback_handler = callback_handler
        self.orientation = 'horizontal'
        self.padding = dp(10)
        self.spacing = dp(10)
        self.size_hint_y = None
        self.height = dp(60)
        
        # Add a border and background
        with self.canvas.before:
            Color(0.2, 0.3, 0.4, 1)  # Dark blue-gray background
            self.rect = Rectangle(pos=self.pos, size=self.size)
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # Run Tests button
        test_button = Button(
            text="Run Tests",
            size_hint_x=0.25,
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        test_button.bind(on_press=callback_handler.show_tests)
        self.add_widget(test_button)
        
        # Administer Treatment button
        treatment_button = Button(
            text="Treatment",
            size_hint_x=0.25,
            background_color=(0.2, 0.7, 0.3, 1),
            background_normal=''
        )
        treatment_button.bind(on_press=callback_handler.show_treatments)
        self.add_widget(treatment_button)
        
        # Diagnose button
        diagnose_button = Button(
            text="Diagnose",
            size_hint_x=0.25,
            background_color=(0.8, 0.6, 0.2, 1),
            background_normal=''
        )
        diagnose_button.bind(on_press=callback_handler.show_diagnosis)
        self.add_widget(diagnose_button)
        
        # Back button
        back_button = Button(
            text="Back",
            size_hint_x=0.25,
            background_color=(0.7, 0.2, 0.2, 1),
            background_normal=''
        )
        back_button.bind(on_press=callback_handler.go_back)
        self.add_widget(back_button)
    
    def update_rect(self, *args):
        """Update rectangle position and size when widget position or size changes."""
        self.rect.pos = self.pos
        self.rect.size = self.size


class PatientViewScreen(Screen):
    """
    Screen for viewing and interacting with a patient.
    Displays vitals, symptoms, and provides options for tests and treatments.
    """
    
    def __init__(self, game_state: GameState, **kwargs):
        """
        Initialize the patient view screen.
        
        Args:
            game_state: Game state manager
            **kwargs: Additional keyword arguments
        """
        super(PatientViewScreen, self).__init__(**kwargs)
        self.game_state = game_state
        
        # Main layout will be populated when a patient is loaded
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.add_widget(self.layout)
    
    def on_pre_enter(self):
        """Called when the screen is about to be displayed."""
        # Clear previous layout
        self.layout.clear_widgets()
        
        # Make sure we have a patient
        if not self.game_state.current_patient:
            self.show_error_popup("No patient loaded", "Returning to main menu")
            self.manager.current = 'main_menu'
            return
        
        # Setup the patient view
        self.setup_patient_view()
    
    def setup_patient_view(self):
        """Set up the patient view with all necessary components."""
        patient = self.game_state.current_patient
        
        # Top section: Header with patient name and specialization
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08)
        
        patient_name_label = Label(
            text=f"Patient: {patient.name}",
            font_size=dp(20),
            bold=True,
            size_hint_x=0.6,
            halign='left',
            color=(0.9, 0.9, 0.9, 1)
        )
        header_layout.add_widget(patient_name_label)
        
        if self.game_state.doctor and self.game_state.doctor.specialization:
            spec_name = self.game_state.doctor.specialization.name
            specialization_label = Label(
                text=f"Specialization: {spec_name}",
                font_size=dp(16),
                size_hint_x=0.4,
                halign='right',
                color=(0.7, 0.8, 0.9, 1)
            )
            header_layout.add_widget(specialization_label)
        
        self.layout.add_widget(header_layout)
        
        # Middle section: Patient info, vitals, and symptoms
        middle_layout = BoxLayout(orientation='horizontal', size_hint_y=0.84, spacing=dp(10))
        
        # Left side: Patient info and symptoms
        left_panel = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=dp(10))
        
        # Patient info
        patient_info = PatientInfoPanel(patient=patient)
        left_panel.add_widget(patient_info)
        
        # Symptoms
        symptoms_panel = SymptomsPanel(patient=patient, size_hint_y=0.7)
        left_panel.add_widget(symptoms_panel)
        
        middle_layout.add_widget(left_panel)
        
        # Right side: Vitals monitor and patient visualization (placeholder for now)
        right_panel = BoxLayout(orientation='vertical', size_hint_x=0.6, spacing=dp(10))
        
        # Vitals monitor
        vitals_monitor = VitalsMonitor(patient=patient)
        right_panel.add_widget(vitals_monitor)
        
        # Patient visualization placeholder (will be improved in later phases)
        patient_visual = BoxLayout(orientation='vertical', size_hint_y=0.7)
        with patient_visual.canvas:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(pos=patient_visual.pos, size=patient_visual.size)
        
        visualization_label = Label(
            text="Patient Visualization\n(Will be implemented in later phases)",
            halign='center',
            valign='middle',
            color=(0.5, 0.5, 0.5, 1)
        )
        patient_visual.add_widget(visualization_label)
        right_panel.add_widget(patient_visual)
        
        middle_layout.add_widget(right_panel)
        
        self.layout.add_widget(middle_layout)
        
        # Bottom section: Action buttons
        action_panel = ActionPanel(callback_handler=self, size_hint_y=0.08)
        self.layout.add_widget(action_panel)
    
    def show_tests(self, instance):
        """
        Show available tests popup.
        
        Args:
            instance: Button instance that triggered the event
        """
        if not self.game_state.doctor or not self.game_state.doctor.specialization:
            self.show_error_popup("No specialization selected", "Please select a specialization first")
            return
        
        # Create popup content
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Header
        header_label = Label(
            text="Available Tests",
            font_size=dp(18),
            bold=True,
            size_hint_y=0.1
        )
        content.add_widget(header_label)
        
        # Scrollable test list
        scroll_view = ScrollView(size_hint=(1, 0.8))
        test_grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        test_grid.bind(minimum_height=test_grid.setter('height'))
        
        # Add tests from doctor's specialization
        available_tests = self.game_state.doctor.specialization.available_tests
        for test in available_tests:
            test_button = Button(
                text=test,
                size_hint_y=None,
                height=dp(50),
                background_color=(0.2, 0.6, 0.8, 1),
                background_normal=''
            )
            test_button.bind(on_press=lambda btn, t=test: self.run_test(t, popup))
            test_grid.add_widget(test_button)
        
        scroll_view.add_widget(test_grid)
        content.add_widget(scroll_view)
        
        # Close button
        close_button = Button(
            text="Close",
            size_hint_y=0.1,
            background_color=(0.7, 0.2, 0.2, 1),
            background_normal=''
        )
        
        popup = Popup(
            title="Medical Tests",
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=True
        )
        
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(close_button)
        
        popup.open()
    
    def run_test(self, test_name, popup):
        """
        Run a selected medical test on the current patient.
        
        Args:
            test_name: Name of the test to run
            popup: The popup to close after running the test
        """
        # Close the test selection popup
        popup.dismiss()
        
        # Run the test on the patient
        result = self.game_state.current_patient.perform_test(test_name)
        
        # Show a placeholder result in Phase 1
        # In Phase 2, this will show actual test results
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Result header
        header_label = Label(
            text=f"{test_name} Results",
            font_size=dp(18),
            bold=True,
            size_hint_y=0.2
        )
        content.add_widget(header_label)
        
        # Result placeholder
        result_label = Label(
            text="Test performed successfully.\nDetailed results will be available in Phase 2.",
            size_hint_y=0.6,
            halign='center',
            valign='middle'
        )
        content.add_widget(result_label)
        
        # Close button
        close_button = Button(
            text="Close",
            size_hint_y=0.2,
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        
        result_popup = Popup(
            title="Test Results",
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=True,
            color=(0.9, 0.9, 0.9, 1),  # Light gray color
        )
        
        close_button.bind(on_press=result_popup.dismiss)
        content.add_widget(close_button)
        
        result_popup.open()
    
    def show_treatments(self, instance):
        """
        Show available treatments popup.
        
        Args:
            instance: Button instance that triggered the event
        """
        if not self.game_state.doctor or not self.game_state.doctor.specialization:
            self.show_error_popup("No specialization selected", "Please select a specialization first")
            return
        
        # Create popup content
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Header
        header_label = Label(
            text="Available Treatments",
            font_size=dp(18),
            bold=True,
            size_hint_y=0.1
        )
        content.add_widget(header_label)
        
        # Scrollable treatment list
        scroll_view = ScrollView(size_hint=(1, 0.8))
        treatment_grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        treatment_grid.bind(minimum_height=treatment_grid.setter('height'))
        
        # Add treatments from doctor's specialization
        available_treatments = self.game_state.doctor.specialization.available_treatments
        for treatment in available_treatments:
            treatment_button = Button(
                text=treatment,
                size_hint_y=None,
                height=dp(50),
                background_color=(0.2, 0.7, 0.3, 1),
                background_normal=''
            )
            treatment_button.bind(on_press=lambda btn, t=treatment: self.apply_treatment(t, popup))
            treatment_grid.add_widget(treatment_button)
        
        scroll_view.add_widget(treatment_grid)
        content.add_widget(scroll_view)
        
        # Close button
        close_button = Button(
            text="Close",
            size_hint_y=0.1,
            background_color=(0.7, 0.2, 0.2, 1),
            background_normal=''
        )
        
        popup = Popup(
            title="Medical Treatments",
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=True
        )
        
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(close_button)
        
        popup.open()
    
    def apply_treatment(self, treatment_name, popup):
        """
        Apply a selected treatment to the current patient.
        
        Args:
            treatment_name: Name of the treatment to apply
            popup: The popup to close after applying the treatment
        """
        # Close the treatment selection popup
        popup.dismiss()
        
        # Apply the treatment to the patient
        result = self.game_state.current_patient.apply_treatment(treatment_name)
        
        # In Phase 1, treatments have no effect. This will be expanded in Phase 2.
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Result header
        header_label = Label(
            text=f"Treatment Applied: {treatment_name}",
            font_size=dp(18),
            bold=True,
            size_hint_y=0.2
        )
        content.add_widget(header_label)
        
        # Result placeholder
        result_label = Label(
            text="Treatment has been applied to the patient.\nPatient response will be simulated in Phase 2.",
            size_hint_y=0.6,
            halign='center',
            valign='middle'
        )
        content.add_widget(result_label)
        
        # Close button
        close_button = Button(
            text="Close",
            size_hint_y=0.2,
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        
        result_popup = Popup(
            title="Treatment Result",
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=True
        )
        
        close_button.bind(on_press=result_popup.dismiss)
        content.add_widget(close_button)
        
        result_popup.open()
    
    def show_diagnosis(self, instance):
        """
        Show diagnosis options popup.
        
        Args:
            instance: Button instance that triggered the event
        """
        # Create popup content
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Header
        header_label = Label(
            text="Make a Diagnosis",
            font_size=dp(18),
            bold=True,
            size_hint_y=0.1
        )
        content.add_widget(header_label)
        
        # For Phase 1, we'll use placeholder diagnoses
        # This will be expanded in Phase 2 to use data from tests
        diagnoses = [
            "Heart Attack", "Pneumonia", "Appendicitis", "Influenza", 
            "Migraine", "Gastroenteritis", "Urinary Tract Infection",
            "Asthma", "Allergic Reaction", "Dehydration"
        ]
        
        # Scrollable diagnosis list
        scroll_view = ScrollView(size_hint=(1, 0.8))
        diagnosis_grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        diagnosis_grid.bind(minimum_height=diagnosis_grid.setter('height'))
        
        for diagnosis in diagnoses:
            diagnosis_button = Button(
                text=diagnosis,
                size_hint_y=None,
                height=dp(50),
                background_color=(0.8, 0.6, 0.2, 1),
                background_normal=''
            )
            diagnosis_button.bind(on_press=lambda btn, d=diagnosis: self.make_diagnosis(d, popup))
            diagnosis_grid.add_widget(diagnosis_button)
        
        scroll_view.add_widget(diagnosis_grid)
        content.add_widget(scroll_view)
        
        # Close button
        close_button = Button(
            text="Cancel",
            size_hint_y=0.1,
            background_color=(0.7, 0.2, 0.2, 1),
            background_normal=''
        )
        
        popup = Popup(
            title="Diagnosis",
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=True
        )
        
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(close_button)
        
        popup.open()
    
    def make_diagnosis(self, diagnosis_name, popup):
        """
        Apply a diagnosis to the current patient.
        
        Args:
            diagnosis_name: Name of the diagnosis
            popup: The popup to close after making the diagnosis
        """
        # Close the diagnosis selection popup
        popup.dismiss()
        
        # Set the diagnosis for the patient
        self.game_state.current_patient.diagnosis = diagnosis_name
        
        # In Phase 1, diagnosis is just stored
        # In Phase 2, it will be checked against the actual condition and affect the patient
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Result header
        header_label = Label(
            text=f"Diagnosis: {diagnosis_name}",
            font_size=dp(18),
            bold=True,
            size_hint_y=0.2
        )
        content.add_widget(header_label)
        
        # Result placeholder
        result_label = Label(
            text="Your diagnosis has been recorded.\nIn Phase 2, this will affect patient outcomes.",
            size_hint_y=0.6,
            halign='center',
            valign='middle'
        )
        content.add_widget(result_label)
        
        # Close button
        close_button = Button(
            text="Close",
            size_hint_y=0.2,
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal=''
        )
        
        result_popup = Popup(
            title="Diagnosis Made",
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=True
        )
        
        close_button.bind(on_press=result_popup.dismiss)
        content.add_widget(close_button)
        
        result_popup.open()
    
    def go_back(self, instance):
        """
        Return to the specialization selection screen.
        
        Args:
            instance: Button instance that triggered the event
        """
        self.manager.current = 'specialization_select'
    
    def show_error_popup(self, title, message):
        """
        Show an error popup with a message.
        
        Args:
            title: Title of the error popup
            message: Error message to display
        """
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Error message
        error_label = Label(
            text=message,
            size_hint_y=0.8,
            halign='center',
            valign='middle'
        )
        content.add_widget(error_label)
        
        # Close button
        close_button = Button(
            text="Close",
            size_hint_y=0.2,
            background_color=(0.7, 0.2, 0.2, 1),
            background_normal=''
        )
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.6, 0.4),
            auto_dismiss=True
        )
        
        close_button.bind(on_press=popup.dismiss)
        content.add_widget(close_button)
        
        popup.open()
