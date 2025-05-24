"""
Test-related screens for the VirtualDoctor application.
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
from kivy.metrics import dp

class TestsScreen(Screen):
    def __init__(self, **kwargs):
        super(TestsScreen, self).__init__(**kwargs)
        self.name = 'tests'
        
        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Title
        title = Label(
            text="Available Tests",
            font_size=24,
            size_hint_y=None,
            height=dp(50)
        )
        layout.add_widget(title)
        
        # Scrollable area for tests
        scroll = ScrollView()
        self.tests_grid = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None,
            padding=10
        )
        self.tests_grid.bind(minimum_height=self.tests_grid.setter('height'))
        scroll.add_widget(self.tests_grid)
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
    
    def update_tests(self):
        """Update the list of available tests based on doctor's specialization"""
        self.tests_grid.clear_widgets()
        
        app = App.get_running_app()
        if not app.game_state.doctor or not app.game_state.doctor.specialization:
            return
        
        # Get available tests from specialization
        available_tests = app.game_state.doctor.specialization.available_tests
        
        for test in available_tests:
            btn = Button(
                text=test,
                size_hint_y=None,
                height=dp(50),
                background_color=(0.2, 0.6, 0.8, 1)
            )
            btn.test_name = test
            btn.bind(on_press=self.run_test)
            self.tests_grid.add_widget(btn)
    
    def run_test(self, instance):
        """Run the selected test"""
        app = App.get_running_app()
        if not app.game_state.current_patient:
            return
        
        # Get test results
        test_name = instance.test_name
        results = app.game_state.run_test(test_name)
        
        # Show results screen
        results_screen = self.manager.get_screen('test_results')
        results_screen.set_test_results(test_name, results)
        self.manager.current = 'test_results'
    
    def go_to_patient(self, instance):
        """Return to patient screen"""
        self.manager.current = 'patient'


class TestResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(TestResultsScreen, self).__init__(**kwargs)
        self.name = 'test_results'
        
        # Main layout
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Title
        self.title = Label(
            text="Test Results",
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
        
        back_btn = Button(
            text="Back to Tests",
            background_color=(0.8, 0.2, 0.2, 1)
        )
        back_btn.bind(on_press=self.go_to_tests)
        btn_layout.add_widget(back_btn)
        
        patient_btn = Button(
            text="Back to Patient",
            background_color=(0.2, 0.6, 0.8, 1)
        )
        patient_btn.bind(on_press=self.go_to_patient)
        btn_layout.add_widget(patient_btn)
        
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def set_test_results(self, test_name, results):
        """Display the test results"""
        self.title.text = f"{test_name} Results"
        
        # Format results for display
        if isinstance(results, dict):
            result_text = ""
            for key, value in results.items():
                result_text += f"{key}: {value}\n"
        else:
            result_text = str(results)
        
        self.results_label.text = result_text
    
    def go_to_tests(self, instance):
        """Return to tests screen"""
        self.manager.current = 'tests'
    
    def go_to_patient(self, instance):
        """Return to patient screen"""
        self.manager.current = 'patient' 