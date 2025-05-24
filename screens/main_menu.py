from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock

from utils.game_state import GameState


class MainMenuScreen(Screen):
    """
    Main menu screen for the VirtualDoctor application.
    Provides navigation to other game modes and features.
    """
    
    def __init__(self, game_state: GameState, **kwargs):
        """
        Initialize the main menu screen.
        
        Args:
            game_state: Game state manager
            **kwargs: Additional keyword arguments
        """
        super(MainMenuScreen, self).__init__(**kwargs)
        self.game_state = game_state
        
        # Create the main layout
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Add title
        title_layout = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        title_label = Label(
            text='VirtualDoctor',
            font_size=dp(36),
            bold=True,
            color=(0.2, 0.6, 0.8, 1)  # Medical blue color
        )
        title_layout.add_widget(title_label)
        self.layout.add_widget(title_layout)
        
        # Add subtitle
        subtitle_label = Label(
            text='Medical Simulation Game',
            font_size=dp(20),
            color=(0.5, 0.5, 0.5, 1)
        )
        self.layout.add_widget(subtitle_label)
        
        # Add spacer
        self.layout.add_widget(BoxLayout(size_hint_y=0.1))
        
        # Add buttons
        button_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=0.5)
        
        # Doctor Mode button
        doctor_button = Button(
            text='Start Doctor Mode',
            font_size=dp(20),
            background_color=(0.2, 0.6, 0.8, 1),
            background_normal='',
            size_hint_y=None,
            height=dp(60)
        )
        doctor_button.bind(on_press=self.start_doctor_mode)
        button_layout.add_widget(doctor_button)
        
        # Settings button
        settings_button = Button(
            text='Settings',
            font_size=dp(20),
            background_color=(0.5, 0.5, 0.5, 1),
            background_normal='',
            size_hint_y=None,
            height=dp(60)
        )
        settings_button.bind(on_press=self.open_settings)
        button_layout.add_widget(settings_button)
        
        # About button
        about_button = Button(
            text='About',
            font_size=dp(20),
            background_color=(0.5, 0.5, 0.5, 1),
            background_normal='',
            size_hint_y=None,
            height=dp(60)
        )
        about_button.bind(on_press=self.open_about)
        button_layout.add_widget(about_button)
        
        # Exit button
        exit_button = Button(
            text='Exit',
            font_size=dp(20),
            background_color=(0.8, 0.2, 0.2, 1),  # Red color
            background_normal='',
            size_hint_y=None,
            height=dp(60)
        )
        exit_button.bind(on_press=self.exit_game)
        button_layout.add_widget(exit_button)
        
        self.layout.add_widget(button_layout)
        
        # Add spacer
        self.layout.add_widget(BoxLayout(size_hint_y=0.1))
        
        # Add footer
        footer_label = Label(
            text='© 2024 VirtualDoctor Team',
            font_size=dp(14),
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=0.1
        )
        self.layout.add_widget(footer_label)
        
        self.add_widget(self.layout)
    
    def start_doctor_mode(self, instance):
        """
        Start the doctor mode, transitioning to specialization selection.
        
        Args:
            instance: Button instance that triggered the event
        """
        self.manager.current = 'specialization_select'
    
    def open_settings(self, instance):
        """
        Open the settings screen (to be implemented in later phases).
        
        Args:
            instance: Button instance that triggered the event
        """
        # Placeholder for future implementation
        pass
    
    def open_about(self, instance):
        """
        Open the about screen with game information (to be implemented in later phases).
        
        Args:
            instance: Button instance that triggered the event
        """
        # Placeholder for future implementation
        pass
    
    def exit_game(self, instance):
        """
        Exit the application.
        
        Args:
            instance: Button instance that triggered the event
        """
        # Schedule the stop event in the next frame to avoid Kivy issues
        Clock.schedule_once(lambda dt: self.stop_app(), 0.1)
    
    def stop_app(self):
        """Stop the application."""
        from kivy.app import App
        App.get_running_app().stop()
