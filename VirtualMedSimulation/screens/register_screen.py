"""
Registration screen for VirtualDoctor
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

from utils.db_manager import DBManager

class RegisterScreen(Screen):
    """Registration screen for the VirtualDoctor application"""
    
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
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
            text="VirtualDoctor Registration",
            font_size=dp(24),
            color=(1, 1, 1, 1),
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
        
        # Registration form
        reg_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(180))
        
        username_label = Label(
            text="Username:",
            color=(0, 0, 0, 1),
            size_hint_x=0.3,
            halign='right'
        )
        self.username_input = TextInput(
            hint_text="Choose a username",
            multiline=False,
            size_hint_x=0.7,
            height=dp(40)
        )
        
        email_label = Label(
            text="Email:",
            color=(0, 0, 0, 1),
            size_hint_x=0.3,
            halign='right'
        )
        self.email_input = TextInput(
            hint_text="Enter your email",
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
            hint_text="Choose a password",
            multiline=False,
            password=True,
            size_hint_x=0.7,
            height=dp(40)
        )
        
        confirm_label = Label(
            text="Confirm Password:",
            color=(0, 0, 0, 1),
            size_hint_x=0.3,
            halign='right'
        )
        self.confirm_input = TextInput(
            hint_text="Confirm your password",
            multiline=False,
            password=True,
            size_hint_x=0.7,
            height=dp(40)
        )
        
        reg_layout.add_widget(username_label)
        reg_layout.add_widget(self.username_input)
        reg_layout.add_widget(email_label)
        reg_layout.add_widget(self.email_input)
        reg_layout.add_widget(password_label)
        reg_layout.add_widget(self.password_input)
        reg_layout.add_widget(confirm_label)
        reg_layout.add_widget(self.confirm_input)
        
        # Button layout
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        register_button = Button(
            text="Register",
            size_hint_x=0.5,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        register_button.bind(on_press=self.register)
        
        cancel_button = Button(
            text="Cancel",
            size_hint_x=0.5,
            background_color=(0.7, 0.3, 0.3, 1)
        )
        cancel_button.bind(on_press=self.go_to_login)
        
        button_layout.add_widget(register_button)
        button_layout.add_widget(cancel_button)
        
        # Status message
        self.status_label = Label(
            text="",
            color=(0.8, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        
        # Add all to form layout
        form_box.add_widget(Label(text="Create a new account", color=(0, 0, 0, 1)))
        form_box.add_widget(reg_layout)
        form_box.add_widget(self.status_label)
        form_box.add_widget(button_layout)
        form_box.add_widget(BoxLayout())  # Spacer
        
        main_layout.add_widget(form_box)
        self.add_widget(main_layout)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def update_form_rect(self, instance, value):
        self.form_rect.pos = instance.pos
        self.form_rect.size = instance.size
    
    def register(self, instance):
        username = self.username_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        confirm = self.confirm_input.text.strip()
        
        # Validate inputs
        if not username or not email or not password or not confirm:
            self.status_label.text = "All fields are required"
            return
        
        if password != confirm:
            self.status_label.text = "Passwords do not match"
            return
        
        if len(password) < 6:
            self.status_label.text = "Password must be at least 6 characters"
            return
        
        if '@' not in email or '.' not in email:
            self.status_label.text = "Invalid email format"
            return
        
        # Register user
        user = DBManager.register_user(username, email, password)
        
        if user:
            # Registration successful
            self.status_label.text = "Registration successful! Please log in."
            self.status_label.color = (0.2, 0.7, 0.2, 1)  # Green
            
            # Clear fields
            self.username_input.text = ""
            self.email_input.text = ""
            self.password_input.text = ""
            self.confirm_input.text = ""
            
            # Go to login after a brief delay
            from kivy.clock import Clock
            Clock.schedule_once(self.go_to_login_delayed, 2)
        else:
            self.status_label.text = "Registration failed. Username or email may already be taken."
    
    def go_to_login_delayed(self, dt):
        self.go_to_login(None)
    
    def go_to_login(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'