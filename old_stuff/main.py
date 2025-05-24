from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

# Define screens
class MainMenu(Screen):
    pass

class ButtonMenu(Screen):
    pass

class PatientInfo(Screen):
    def set_patient(self, patient_id):
        self.ids.info_label.text = f"Showing info for Patient #{patient_id}"

# Set up screen manager
class VirtualDoctorApp(App):
    def build(self):
        return Builder.load_file("virtualdoctor.kv")


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

if __name__ == '__main__':
    VirtualDoctorApp().run()
