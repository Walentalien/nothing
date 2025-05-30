"""
Dashboard screen for VirtualDoctor showing user statistics and progress
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

from utils.db_manager import DBManager

class DashboardScreen(Screen):
    """User dashboard showing game statistics and progress"""
    
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        self.user = None
        self.create_ui()
        
    def create_ui(self):
        # Main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Add title with background
        title_box = BoxLayout(size_hint_y=0.15)
        with title_box.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Medical blue
            self.rect = Rectangle(pos=title_box.pos, size=title_box.size)
        title_box.bind(pos=self.update_rect, size=self.update_rect)
        
        self.title_label = Label(
            text="User Dashboard",
            font_size=dp(24),
            color=(0.2, 0.2, 0.2, 1),  # Dark gray color
            bold=True
        )
        title_box.add_widget(self.title_label)
        self.main_layout.add_widget(title_box)
        
        # Dashboard content with scrolling
        scroll_view = ScrollView(do_scroll_x=False, do_scroll_y=True)
        self.dashboard_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None)
        self.dashboard_layout.bind(minimum_height=self.dashboard_layout.setter('height'))
        
        # Stats section
        self.stats_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(200))
        self.stats_layout.add_widget(Label(text="Username:", color=(0.2, 0.2, 0.2, 1), bold=True, size_hint_x=0.4))
        self.username_label = Label(text="Loading...", color=(0.2, 0.2, 0.2, 1), size_hint_x=0.6)
        self.stats_layout.add_widget(self.username_label)
        
        self.stats_layout.add_widget(Label(text="Email:", color=(0.2, 0.2, 0.2, 1), bold=True, size_hint_x=0.4))
        self.email_label = Label(text="Loading...", color=(0.2, 0.2, 0.2, 1), size_hint_x=0.6)
        self.stats_layout.add_widget(self.email_label)
        
        self.stats_layout.add_widget(Label(text="Account Created:", color=(0.2, 0.2, 0.2, 1), bold=True, size_hint_x=0.4))
        self.created_label = Label(text="Loading...", color=(0.2, 0.2, 0.2, 1), size_hint_x=0.6)
        self.stats_layout.add_widget(self.created_label)
        
        self.stats_layout.add_widget(Label(text="Last Login:", color=(0.2, 0.2, 0.2, 1), bold=True, size_hint_x=0.4))
        self.last_login_label = Label(text="Loading...", color=(0.2, 0.2, 0.2, 1), size_hint_x=0.6)
        self.stats_layout.add_widget(self.last_login_label)
        
        # Game progress section
        self.progress_label = Label(
            text="Game Progress",
            font_size=dp(18),
            color=(0.2, 0.6, 0.8, 1),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        
        # Progress container
        self.progress_container = GridLayout(cols=1, spacing=dp(15), size_hint_y=None)
        self.progress_container.bind(minimum_height=self.progress_container.setter('height'))
        
        # Add gameplay statistics
        self.stats_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(200))
        with self.stats_box.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Light gray
            self.stats_rect = Rectangle(pos=self.stats_box.pos, size=self.stats_box.size)
        self.stats_box.bind(pos=self.update_stats_rect, size=self.update_stats_rect)
        
        self.stats_header = Label(
            text="Gameplay Statistics",
            font_size=dp(18),
            color=(0.2, 0.6, 0.8, 1),
            bold=True,
            size_hint_y=None,
            height=dp(40)
        )
        
        self.stats_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(150))
        self.stats_grid.add_widget(Label(text="Total Patients Treated:", color=(0.2, 0.2, 0.2, 1), bold=True, size_hint_x=0.6))
        self.patients_treated_label = Label(text="0", color=(0.2, 0.2, 0.2, 1), size_hint_x=0.4)
        self.stats_grid.add_widget(self.patients_treated_label)
        
        self.stats_grid.add_widget(Label(text="Successful Diagnoses:", color=(0.2, 0.2, 0.2, 1), bold=True, size_hint_x=0.6))
        self.successful_diagnoses_label = Label(text="0", color=(0.2, 0.2, 0.2, 1), size_hint_x=0.4)
        self.stats_grid.add_widget(self.successful_diagnoses_label)
        
        self.stats_grid.add_widget(Label(text="Current Level:", color=(0.2, 0.2, 0.2, 1), bold=True, size_hint_x=0.6))
        self.level_label = Label(text="1", color=(0.2, 0.2, 0.2, 1), size_hint_x=0.4)
        self.stats_grid.add_widget(self.level_label)
        
        self.stats_grid.add_widget(Label(text="Score:", color=(0.2, 0.2, 0.2, 1), bold=True, size_hint_x=0.6))
        self.score_label = Label(text="0", color=(0.2, 0.2, 0.2, 1), size_hint_x=0.4)
        self.stats_grid.add_widget(self.score_label)
        
        self.stats_box.add_widget(self.stats_header)
        self.stats_box.add_widget(self.stats_grid)
        
        # Button layout
        button_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        
        continue_button = Button(
            text="Continue Game",
            size_hint_x=0.5,
            background_color=(0.2, 0.7, 0.3, 1)
        )
        continue_button.bind(on_press=self.continue_game)
        
        logout_button = Button(
            text="Logout",
            size_hint_x=0.5,
            background_color=(0.7, 0.3, 0.3, 1)
        )
        logout_button.bind(on_press=self.logout)
        
        button_layout.add_widget(continue_button)
        button_layout.add_widget(logout_button)
        
        # Add all elements to layouts
        self.dashboard_layout.add_widget(self.stats_layout)
        self.dashboard_layout.add_widget(self.progress_label)
        self.dashboard_layout.add_widget(self.progress_container)
        self.dashboard_layout.add_widget(self.stats_box)
        self.dashboard_layout.add_widget(button_layout)
        
        scroll_view.add_widget(self.dashboard_layout)
        self.main_layout.add_widget(scroll_view)
        
        self.add_widget(self.main_layout)
    
    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def update_stats_rect(self, instance, value):
        self.stats_rect.pos = instance.pos
        self.stats_rect.size = instance.size
    
    def update_for_user(self, user):
        """Update dashboard with user data"""
        if not user:
            return
            
        self.user = user
        
        # Update title
        self.title_label.text = f"Welcome, {user['username']}"
        
        # Update user info
        self.username_label.text = user['username']
        self.email_label.text = user['email']
        self.created_label.text = str(user.get('created_at', 'N/A'))
        self.last_login_label.text = str(user.get('last_login', 'N/A'))
        
        # Get user progress
        progress_data = DBManager.get_user_progress(user['id'])
        
        # Clear existing progress items
        self.progress_container.clear_widgets()
        
        if progress_data:
            # Show progress for each saved character/doctor
            for progress in progress_data:
                progress_box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), padding=dp(10))
                with progress_box.canvas.before:
                    Color(0.9, 0.95, 1, 1)  # Light blue
                    Rectangle(pos=progress_box.pos, size=progress_box.size)
                
                progress_box.add_widget(Label(
                    text=f"Specialization: {progress.get('current_specialization', 'General')}",
                    color=(0, 0, 0, 1),
                    bold=True
                ))
                
                details_grid = GridLayout(cols=2, spacing=dp(5))
                details_grid.add_widget(Label(text="Level:", color=(0, 0, 0, 1), size_hint_x=0.4, halign='right'))
                details_grid.add_widget(Label(text=str(progress.get('level', 1)), color=(0, 0, 0, 1), size_hint_x=0.6, halign='left'))
                
                details_grid.add_widget(Label(text="Score:", color=(0, 0, 0, 1), size_hint_x=0.4, halign='right'))
                details_grid.add_widget(Label(text=str(progress.get('score', 0)), color=(0, 0, 0, 1), size_hint_x=0.6, halign='left'))
                
                details_grid.add_widget(Label(text="Cases Completed:", color=(0, 0, 0, 1), size_hint_x=0.4, halign='right'))
                details_grid.add_widget(Label(text=str(progress.get('completed_cases', 0)), color=(0, 0, 0, 1), size_hint_x=0.6, halign='left'))
                
                progress_box.add_widget(details_grid)
                self.progress_container.add_widget(progress_box)
                
                # Update the global stats
                self.patients_treated_label.text = str(progress.get('completed_cases', 0))
                self.level_label.text = str(progress.get('level', 1))
                self.score_label.text = str(progress.get('score', 0))
        else:
            # No progress yet
            no_progress = Label(
                text="No game progress yet. Start playing to see your statistics!",
                color=(0.2, 0.2, 0.2, 1),
                size_hint_y=None,
                height=dp(40)
            )
            self.progress_container.add_widget(no_progress)
    
    def continue_game(self, instance):
        """Continue the game from where the user left off"""
        self.manager.transition.direction = 'left'
        self.manager.current = 'specialization'
    
    def logout(self, instance):
        """Log out the user"""
        app = self.get_root_window().children[0]
        app.current_user = None
        
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_menu'