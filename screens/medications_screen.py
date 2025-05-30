"""
Medications Screen for VirtualDoctor
Allows selection and administration of medications to patients
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
from kivy.app import App
try:
    from utils.medication_manager import MedicationManager
except ImportError:
    pass # Handle the error as needed, perhaps by providing a mock MedicationManager

# Use the local medication manager
from utils.medication_manager import MedicationManager

class MedicationsScreen(Screen):
    def __init__(self, **kwargs):
        super(MedicationsScreen, self).__init__(**kwargs)
        self.name = 'medications'

        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add header
        self.header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

        # Back button
        self.back_btn = Button(text='Back to Patient', size_hint=(0.3, 1))
        self.back_btn.bind(on_release=self.go_to_patient)
        self.header.add_widget(self.back_btn)

        # Title
        self.title = Label(text='Medications', font_size=24, size_hint=(0.7, 1))
        self.header.add_widget(self.title)

        self.layout.add_widget(self.header)

        # Content area
        self.content = BoxLayout(orientation='vertical', spacing=10)

        # Categories and medications
        self.categories_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)

        # Category selector
        self.category_label = Label(text='Category:', size_hint=(0.3, 1))
        self.categories_row.add_widget(self.category_label)

        self.category_spinner = Spinner(
            text='All',
            values=['All', 'Antibiotic', 'Painkiller', 'Antihypertensive', 'Bronchodilator', 'Antidiabetic'],
            size_hint=(0.7, 1)
        )
        self.category_spinner.bind(text=self.update_medications)
        self.categories_row.add_widget(self.category_spinner)

        self.content.add_widget(self.categories_row)

        # Medications list
        self.medications_layout = GridLayout(cols=1, spacing=5, size_hint=(1, 0.5))
        self.medications_layout.bind(minimum_height=self.medications_layout.setter('height'))
        self.content.add_widget(self.medications_layout)

        # Medication administration
        self.admin_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.35), spacing=5)

        # Selected medication info
        self.selected_med_label = Label(text='No medication selected', size_hint=(1, 0.2))
        self.admin_layout.add_widget(self.selected_med_label)

        # Dosage and route selection
        self.dosage_route_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.3), spacing=10)

        # Dosage
        self.dosage_label = Label(text='Dosage:', size_hint=(0.3, 1))
        self.dosage_route_layout.add_widget(self.dosage_label)

        self.dosage_spinner = Spinner(
            text='Select dosage',
            values=[],
            size_hint=(0.7, 1)
        )
        self.dosage_route_layout.add_widget(self.dosage_spinner)

        self.admin_layout.add_widget(self.dosage_route_layout)

        # Route
        self.route_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.3), spacing=10)

        self.route_label = Label(text='Route:', size_hint=(0.3, 1))
        self.route_layout.add_widget(self.route_label)

        self.route_spinner = Spinner(
            text='Select route',
            values=[],
            size_hint=(0.7, 1)
        )
        self.route_layout.add_widget(self.route_spinner)

        self.admin_layout.add_widget(self.route_layout)

        # Administer button
        self.administer_btn = Button(
            text='Administer Medication', 
            size_hint=(1, 0.3),
            background_color=(0.2, 0.7, 0.3, 1)
        )
        self.administer_btn.bind(on_release=self.administer_medication)
        self.admin_layout.add_widget(self.administer_btn)

        self.content.add_widget(self.admin_layout)

        # Response area
        self.response_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3))
        self.response_label = Label(
            text='',
            size_hint=(1, 1),
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        self.response_label.bind(size=self.response_label.setter('text_size'))
        self.response_layout.add_widget(self.response_label)

        self.content.add_widget(self.response_layout)

        self.layout.add_widget(self.content)

        # Next patient button
        self.next_btn = Button(
            text='Return to Patient',
            size_hint=(1, 0.1),
            background_color=(0.3, 0.5, 0.9, 1)
        )
        self.next_btn.bind(on_release=self.go_to_patient)
        self.layout.add_widget(self.next_btn)

        self.add_widget(self.layout)

        # Currently selected medication
        self.selected_medication = None

    def update_for_patient(self):
        """Update the screen for the current patient"""
        app = App.get_running_app()
        if app.game_state and app.game_state.current_patient:
            patient = app.game_state.current_patient
            self.title.text = f'Medications - {patient.name}'

        # Populate medications list
        self.update_medications()

    def update_medications(self, *args):
        """Update the medications list based on selected category"""
        # Clear current list
        self.medications_layout.clear_widgets()

        # Get medications based on category
        if hasattr(self, 'category_spinner') and self.category_spinner.text != 'All':
            medications = MedicationManager.get_medications_by_category(self.category_spinner.text)
        else:
            medications = MedicationManager.get_all_medications()

        # Add medications to the list
        for med in medications:
            med_btn = Button(
                text=med['name'],
                size_hint=(1, None),
                height=40
            )
            med_btn.medication = med
            med_btn.bind(on_release=self.select_medication)
            self.medications_layout.add_widget(med_btn)

        # Clear selection
        self.selected_medication = None
        self.selected_med_label.text = 'No medication selected'
        self.dosage_spinner.values = []
        self.dosage_spinner.text = 'Select dosage'
        self.route_spinner.values = []
        self.route_spinner.text = 'Select route'
        self.response_label.text = ''

    def select_medication(self, instance):
        """Handle medication selection"""
        self.selected_medication = instance.medication
        self.selected_med_label.text = f"Selected: {self.selected_medication['name']} ({self.selected_medication['category']})"

        # Update dosage spinner
        self.dosage_spinner.values = self.selected_medication['dosages']
        if self.dosage_spinner.values:
            self.dosage_spinner.text = self.dosage_spinner.values[0]
        else:
            self.dosage_spinner.text = 'No dosages available'

        # Update route spinner
        self.route_spinner.values = self.selected_medication['administration_routes']
        if self.route_spinner.values:
            self.route_spinner.text = self.route_spinner.values[0]
        else:
            self.route_spinner.text = 'No routes available'

    def administer_medication(self, instance):
        """Administer the selected medication to the current patient"""
        app = App.get_running_app()

        if not app.game_state or not app.game_state.current_patient:
            self.response_label.text = 'Error: No patient selected'
            return

        if not self.selected_medication:
            self.response_label.text = 'Error: No medication selected'
            return

        if self.dosage_spinner.text == 'Select dosage' or self.dosage_spinner.text == 'No dosages available':
            self.response_label.text = 'Error: No dosage selected'
            return

        if self.route_spinner.text == 'Select route' or self.route_spinner.text == 'No routes available':
            self.response_label.text = 'Error: No administration route selected'
            return

        # Administer the medication
        result = MedicationManager.administer_medication(
            app.game_state.current_patient,
            self.selected_medication['name'],
            self.dosage_spinner.text,
            self.route_spinner.text
        )

        if result['success']:
            # Format and display response
            response_text = f"Administered {result['medication']} {result['dosage']} {result['route']}\n\n"
            response_text += f"Effectiveness: {result['effectiveness']:.2f}\n\n"

            if result['side_effects']:
                response_text += "Side effects:\n"
                for effect in result['side_effects']:
                    response_text += f"- {effect['name']} ({effect['severity']})\n"
                response_text += "\n"

            if result['vital_changes']:
                response_text += "Vital signs changes:\n"
                for vital, change in result['vital_changes'].items():
                    if abs(change) > 0.01:  # Only show significant changes
                        response_text += f"- {vital}: {'+' if change > 0 else ''}{change:.1f}\n"
                response_text += "\n"

            response_text += result['response_text']

            self.response_label.text = response_text

            # Update patient in game state with new vital signs
            app.game_state.update_current_patient()
        else:
            self.response_label.text = f"Error: {result['error']}"

    def go_to_patient(self, instance):
        """Go back to the patient screen"""
        self.manager.transition.direction = 'right'
        self.manager.current = 'patient'

    def on_pre_enter(self):
        """Called before the screen is displayed"""
        self.update_for_patient()