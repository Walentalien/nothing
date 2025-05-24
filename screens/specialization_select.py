from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

from models.doctor import Doctor, get_available_specializations
from utils.game_state import GameState


class SpecializationSelectScreen(Screen):
    """
    Screen for selecting a medical specialization for the player's doctor character.
    """
    
    def __init__(self, game_state: GameState, **kwargs):
        """
        Initialize the specialization selection screen.
        
        Args:
            game_state: Game state manager
            **kwargs: Additional keyword arguments
        """
        super(SpecializationSelectScreen, self).__init__(**kwargs)
        self.game_state = game_state
        self.selected_specialization = None
        
        # Create main layout
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Add header
        header_label = Label(
            text='Select Your Specialization',
            font_size=dp(28),
            bold=True,
            size_hint_y=0.1,
            color=(0.2, 0.6, 0.8, 1)  # Medical blue color
        )
        self.layout.add_widget(header_label)
        
        # Add instructions
        instructions_label = Label(
            text='Choose a medical specialty that determines your available tests and treatments',
            font_size=dp(16),
            size_hint_y=0.05,
            color=(0.5, 0.5, 0.5, 1)
        )
        self.layout.add_widget(instructions_label)
        
        # Create a scrollable area for specializations
        scroll_view = ScrollView(size_hint=(1, 0.7), do_scroll_x=False)
        self.specialization_grid = GridLayout(
            cols=1, 
            spacing=dp(10), 
            size_hint_y=None,
            padding=dp(10)
        )
        self.specialization_grid.bind(minimum_height=self.specialization_grid.setter('height'))
        
        # Get available specializations and add them to the grid
        specializations = get_available_specializations()
        for specialization in specializations:
            spec_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(180),
                padding=dp(10),
                spacing=dp(5)
            )
            spec_layout.background_color = (0.95, 0.95, 0.95, 1)
            
            # Specialization name
            name_label = Label(
                text=specialization.name,
                font_size=dp(22),
                bold=True,
                size_hint_y=0.2,
                color=(0.2, 0.6, 0.8, 1)
            )
            spec_layout.add_widget(name_label)
            
            # Specialization description
            desc_label = Label(
                text=specialization.description,
                font_size=dp(14),
                size_hint_y=0.3,
                text_size=(dp(400), None),
                halign='center',
                valign='middle'
            )
            spec_layout.add_widget(desc_label)
            
            # Available tests
            test_label = Label(
                text=f"Tests: {', '.join(specialization.available_tests[:3])}...",
                font_size=dp(12),
                size_hint_y=0.2,
                color=(0.4, 0.4, 0.4, 1)
            )
            spec_layout.add_widget(test_label)
            
            # Available treatments
            treatment_label = Label(
                text=f"Treatments: {', '.join(specialization.available_treatments[:3])}...",
                font_size=dp(12),
                size_hint_y=0.2,
                color=(0.4, 0.4, 0.4, 1)
            )
            spec_layout.add_widget(treatment_label)
            
            # Select button
            select_button = Button(
                text='Select',
                size_hint_y=0.2,
                background_color=(0.2, 0.6, 0.8, 1),
                background_normal=''
            )
            select_button.specialization = specialization  # Store the specialization with the button
            select_button.bind(on_press=self.on_specialization_selected)
            spec_layout.add_widget(select_button)
            
            # Add a border around the specialization layout
            border_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(180),
                padding=dp(2)
            )
            border_layout.add_widget(spec_layout)
            
            self.specialization_grid.add_widget(border_layout)
        
        scroll_view.add_widget(self.specialization_grid)
        self.layout.add_widget(scroll_view)
        
        # Create bottom navigation buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=dp(20))
        
        # Back button
        back_button = Button(
            text='Back',
            size_hint_x=0.5,
            background_color=(0.5, 0.5, 0.5, 1),
            background_normal=''
        )
        back_button.bind(on_press=self.go_back)
        button_layout.add_widget(back_button)
        
        # Continue button (disabled until a specialization is selected)
        self.continue_button = Button(
            text='Continue',
            size_hint_x=0.5,
            background_color=(0.2, 0.6, 0.8, 0.5),  # Dimmed until enabled
            background_normal='',
            disabled=True
        )
        self.continue_button.bind(on_press=self.continue_to_patient)
        button_layout.add_widget(self.continue_button)
        
        self.layout.add_widget(button_layout)
        
        self.add_widget(self.layout)
    
    def on_specialization_selected(self, instance):
        """
        Handle specialization selection.
        
        Args:
            instance: Button instance that triggered the event
        """
        self.selected_specialization = instance.specialization
        
        # Update button appearances - highlight the selected one
        for child in self.specialization_grid.children:
            if isinstance(child, BoxLayout):  # This is the border layout
                for subchild in child.children:
                    if isinstance(subchild, BoxLayout):  # This is the spec_layout
                        # Find the select button in this layout
                        for widget in subchild.children:
                            if isinstance(widget, Button) and hasattr(widget, 'specialization'):
                                if widget.specialization.name == self.selected_specialization.name:
                                    widget.background_color = (0.1, 0.8, 0.1, 1)  # Green for selected
                                    widget.text = 'Selected'
                                else:
                                    widget.background_color = (0.2, 0.6, 0.8, 1)  # Default blue
                                    widget.text = 'Select'
        
        # Enable the continue button
        self.continue_button.disabled = False
        self.continue_button.background_color = (0.2, 0.6, 0.8, 1)  # Full opacity when enabled
    
    def go_back(self, instance):
        """
        Return to the main menu.
        
        Args:
            instance: Button instance that triggered the event
        """
        self.manager.current = 'main_menu'
    
    def continue_to_patient(self, instance):
        """
        Continue to patient screen after selecting a specialization.
        
        Args:
            instance: Button instance that triggered the event
        """
        if self.selected_specialization:
            # Create a new doctor with the selected specialization if one doesn't exist
            if not self.game_state.doctor:
                self.game_state.doctor = Doctor(name="Dr. Player", specialization=self.selected_specialization)
            else:
                # Update existing doctor with the new specialization
                self.game_state.doctor.set_specialization(self.selected_specialization)
            
            # Load a patient from the available data
            self.game_state.load_random_patient()
            
            # Navigate to the patient view
            self.manager.current = 'patient_view'
    
    def on_pre_enter(self):
        """Called when the screen is about to be displayed."""
        # Reset selection when entering the screen
        self.selected_specialization = None
        self.continue_button.disabled = True
        self.continue_button.background_color = (0.2, 0.6, 0.8, 0.5)  # Dimmed until enabled
        
        # Reset button appearances
        for child in self.specialization_grid.children:
            if isinstance(child, BoxLayout):  # This is the border layout
                for subchild in child.children:
                    if isinstance(subchild, BoxLayout):  # This is the spec_layout
                        # Find the select button in this layout
                        for widget in subchild.children:
                            if isinstance(widget, Button) and hasattr(widget, 'specialization'):
                                widget.background_color = (0.2, 0.6, 0.8, 1)  # Default blue
                                widget.text = 'Select'
