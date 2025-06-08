"""
Treatment-related screens for the VirtualDoctor application.
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.metrics import dp

class TreatmentsScreen(Screen):
    def __init__(self, **kwargs):
        super(TreatmentsScreen, self).__init__(**kwargs)
        self.name = 'treatments'
        
        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Title
        title = Label(
            text="Available Treatments",
            font_size=24,
            size_hint_y=None,
            height=dp(50),
            color=(0.9, 0.9, 0.9, 1)
        )
        layout.add_widget(title)
        
        # Scrollable area for treatments
        scroll = ScrollView()
        self.treatments_grid = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=10
        )
        self.treatments_grid.bind(minimum_height=self.treatments_grid.setter('height'))
        scroll.add_widget(self.treatments_grid)
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
    
    def update_treatments(self):
        """Update the list of available treatments based on doctor's specialization"""
        self.treatments_grid.clear_widgets()
        
        app = App.get_running_app()
        if not app.game_state.doctor or not app.game_state.doctor.specialization:
            return
        
        # Get available treatments from specialization
        available_treatments = app.game_state.doctor.specialization.available_treatments
        
        for treatment in available_treatments:
            btn = Button(
                text=treatment,
                size_hint_y=None,
                height=dp(50),
                background_color=(0.2, 0.6, 0.8, 1)
            )
            btn.treatment_name = treatment
            btn.bind(on_press=self.apply_treatment)
            self.treatments_grid.add_widget(btn)
    
    def apply_treatment(self, instance):
        """Apply the selected treatment"""
        app = App.get_running_app()
        if not app.game_state.current_patient:
            return
        
        # Get treatment results
        treatment_name = instance.treatment_name
        results = app.game_state.apply_treatment(treatment_name)
        
        # Show results screen
        results_screen = self.manager.get_screen('treatment_results')
        results_screen.set_treatment_results(treatment_name, results)
        self.manager.current = 'treatment_results'
    
    def go_to_patient(self, instance):
        """Return to patient screen"""
        self.manager.current = 'patient'


class TreatmentResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(TreatmentResultsScreen, self).__init__(**kwargs)
        self.name = 'treatment_results'
        
        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Title
        self.title = Label(
            text="Treatment Results",
            font_size=24,
            size_hint_y=None,
            height=dp(50),
            color=(0.2, 0.2, 0.2, 1)
        )
        layout.add_widget(self.title)
        
        # Results area
        self.results_label = Label(
            text="",
            font_size=16,
            size_hint_y=0.8,
            halign='left',
            valign='top',
            color=(0.2, 0.2, 0.2, 1)
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
        
        back_btn = Button(
            text="Back to Treatments",
            background_color=(0.8, 0.2, 0.2, 1)
        )
        back_btn.bind(on_press=self.go_to_treatments)
        btn_layout.add_widget(back_btn)
        
        patient_btn = Button(
            text="Back to Patient",
            background_color=(0.2, 0.6, 0.8, 1)
        )
        patient_btn.bind(on_press=self.go_to_patient)
        btn_layout.add_widget(patient_btn)
        
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def set_treatment_results(self, treatment_name, results):
        """Display the treatment results"""
        self.title.text = f"{treatment_name} Results"
        
        # Format results for display
        if isinstance(results, dict):
            result_text = ""
            for key, value in results.items():
                result_text += f"{key}: {value}\n"
        else:
            result_text = str(results)
        
        self.results_label.text = result_text
    
    def go_to_treatments(self, instance):
        """Return to treatments screen"""
        self.manager.current = 'treatments'
    
    def go_to_patient(self, instance):
        """Return to patient screen"""
        self.manager.current = 'patient' 