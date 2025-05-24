"""
Diagnosis-related screens for the VirtualDoctor application.
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.metrics import dp

class DiagnosisScreen(Screen):
    def __init__(self, **kwargs):
        super(DiagnosisScreen, self).__init__(**kwargs)
        self.name = 'diagnosis'
        
        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Title
        title = Label(
            text="Make a Diagnosis",
            font_size=24,
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(title)
        
        # Scrollable area for diagnoses
        scroll = ScrollView()
        self.diagnoses_grid = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=10
        )
        self.diagnoses_grid.bind(minimum_height=self.diagnoses_grid.setter('height'))
        scroll.add_widget(self.diagnoses_grid)
        layout.add_widget(scroll)
        
        # Back button
        back_btn = Button(
            text="Back to Patient",
            size_hint_y=None,
            height=dp(50),
            background_color=(0.8, 0.2, 0.2, 1)
        )
        back_btn.bind(on_press=self.go_to_patient)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def update_diagnoses(self):
        """Update the list of possible diagnoses"""
        self.diagnoses_grid.clear_widgets()
        
        app = App.get_running_app()
        if not app.game_state.current_patient:
            return
        
        # Get possible diagnoses based on symptoms and tests
        possible_diagnoses = app.game_state.get_possible_diagnoses()
        
        for diagnosis in possible_diagnoses:
            btn = Button(
                text=diagnosis,
                size_hint_y=None,
                height=dp(50),
                background_color=(0.2, 0.6, 0.8, 1)
            )
            btn.diagnosis = diagnosis
            btn.bind(on_press=self.make_diagnosis)
            self.diagnoses_grid.add_widget(btn)
    
    def make_diagnosis(self, instance):
        """Make the selected diagnosis"""
        app = App.get_running_app()
        if not app.game_state.current_patient:
            return
        
        # Check if diagnosis is correct
        diagnosis = instance.diagnosis
        is_correct = app.game_state.check_diagnosis(diagnosis)
        
        # Show results screen
        results_screen = self.manager.get_screen('diagnosis_results')
        results_screen.set_diagnosis_results(diagnosis, is_correct)
        self.manager.current = 'diagnosis_results'
    
    def go_to_patient(self, instance):
        """Return to patient screen"""
        self.manager.current = 'patient'


class DiagnosisResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(DiagnosisResultsScreen, self).__init__(**kwargs)
        self.name = 'diagnosis_results'
        
        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Title
        self.title = Label(
            text="Diagnosis Results",
            font_size=24,
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(self.title)
        
        # Results area
        self.results_label = Label(
            text="",
            font_size=16,
            size_hint_y=0.8,
            halign='left',
            valign='top'
        )
        self.results_label.bind(size=self.results_label.setter('text_size'))
        layout.add_widget(self.results_label)
        
        # Navigation buttons
        btn_layout = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=dp(50)
        )
        
        patient_btn = Button(
            text="Back to Patient",
            background_color=(0.2, 0.6, 0.8, 1)
        )
        patient_btn.bind(on_press=self.go_to_patient)
        btn_layout.add_widget(patient_btn)
        
        next_btn = Button(
            text="Next Patient",
            background_color=(0.2, 0.8, 0.2, 1)
        )
        next_btn.bind(on_press=self.next_patient)
        btn_layout.add_widget(next_btn)
        
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def set_diagnosis_results(self, diagnosis, is_correct):
        """Display the diagnosis results"""
        self.title.text = "Diagnosis Results"
        
        if is_correct:
            result_text = f"Correct diagnosis! The patient has {diagnosis}."
        else:
            result_text = f"Incorrect diagnosis. The patient does not have {diagnosis}."
        
        self.results_label.text = result_text
    
    def go_to_patient(self, instance):
        """Return to patient screen"""
        self.manager.current = 'patient'
    
    def next_patient(self, instance):
        """Move to next patient"""
        app = App.get_running_app()
        app.game_state.complete_current_case()
        app.game_state.load_random_patient()
        
        # Update patient screen and return to it
        patient_screen = self.manager.get_screen('patient')
        patient_screen.update_patient_data()
        self.manager.current = 'patient' 