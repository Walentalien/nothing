"""
Login and registration screen for VirtualDoctor
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

from utils.db_manager import DBManager

class LoginScreen(Screen):
    """Login screen for the VirtualDoctor application"""
    
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.create_ui()
        
    def create_ui(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Add title with background
        title_box = BoxLayout(size_hint_y=0.15)
        with title_box.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Medical blue
            self.rect = Rectangle(pos=title_box.pos, size=title_box.size)
        title_box.bind(pos=self.update_rect, size=self.update_rect)
        
        title = Label(
            text="VirtualDoctor Login",
            font_size=dp(24),
            color=(0.2, 0.2, 0.2, 1),
            bold=True
        )
        title_box.add_widget(title)
        main_layout.add_widget(title_box)
        
        # Add form container with white background
        form_box = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15), size_hint_y=0.7)
        with form_box.canvas.before:
            Color(1, 1, 1, 1)  # White
            self.form_rect = Rectangle(pos=form_box.pos, size=form_box.size)
        form_box.bind(pos=self.update_form_rect, size=self.update_form_rect)
        
        # Login form
        login_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(100))
        
        username_label = Label(
            text="Username:",
            color=(0, 0, 0, 1),
            size_hint_x=0.3,
            halign='right'
        )
        self.username_input = TextInput(
            hint_text="Enter your username",
            multiline=False,
            size_hint_x=0.7,
            height=dp(40)
        )
        
        password_label = Label(
            text="Password:",
            color=(0, 0, 0, 1),
            size_hint_x=0.3,
            halign='right'
        )
        self.password_input = TextInput(
            hint_text="Enter your password",
            multiline=False,
            password=True,
            size_hint_x=0.7,
            height=dp(40)
        )
        
        login_layout.add_widget(username_label)
        login_layout.add_widget(self.username_input)
        login_layout.add_widget(password_label)
        login_layout.add_widget(self.password_input)
        
        # Button layout
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        login_button = Button(
            text="Login",
            size_hint_x=0.5,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        login_button.bind(on_press=self.login)
        
        register_button = Button(
            text="Register",
            size_hint_x=0.5,
            background_color=(0.3, 0.5, 0.7, 1)
        )
        register_button.bind(on_press=self.go_to_register)
        
        button_layout.add_widget(login_button)
        button_layout.add_widget(register_button)
        
        # Cancel button
        cancel_button = Button(
            text="Cancel",
            size_hint_y=None,
            height=dp(40),
            background_color=(0.7, 0.3, 0.3, 1)
        )
        cancel_button.bind(on_press=self.go_to_main)
        
        # Status message
        self.status_label = Label(
            text="",
            color=(0.8, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        
        # Add all to form layout
        form_box.add_widget(Label(text="Enter your credentials", color=(0.2, 0.2, 0.2, 1)))
        form_box.add_widget(login_layout)
        form_box.add_widget(self.status_label)
        form_box.add_widget(button_layout)
        form_box.add_widget(cancel_button)
        form_box.add_widget(BoxLayout())  # Spacer
        
        main_layout.add_widget(form_box)
        self.add_widget(main_layout)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def update_form_rect(self, instance, value):
        self.form_rect.pos = instance.pos
        self.form_rect.size = instance.size
    
    def login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        if not username or not password:
            self.status_label.text = "Username and password are required"
            return
        
        # Authenticate user
        user = DBManager.authenticate_user(username, password)
        
        if user:
            # Login successful
            app = App.get_running_app()
            app.current_user = user
            
            # The authenticate_user method already updates last login time
            
            # Update the main menu screen
            self.manager.get_screen('main_menu').update_for_logged_user(user)
            
            # Go to dashboard
            self.manager.get_screen('dashboard').update_for_user(user)
            self.manager.transition.direction = 'left'
            self.manager.current = 'dashboard'
        else:
            self.status_label.text = "Invalid username or password"
    
    def go_to_register(self, instance):
        self.manager.transition.direction = 'left'
        self.manager.current = 'register'
    
    def go_to_main(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_menu'