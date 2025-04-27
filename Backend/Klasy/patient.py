
class Patient:
    def __init__(self,name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.parameters = {
            "pulse": 80,
            "systolic_pressure": 50,
            "diastolic_pressure": 100,
            "temperature": 35.6,
            "weight": 70,
            "height": 170,
            "sp_o2": 98,
            "symptoms": []
        }

    def set_parameters(self, pulse, systolic_pressure, diastolic_pressure, temperature,weight, height, sp_o2):
        self.parameters["pulse"] = pulse
        self.parameters["systolic_pressure"] = systolic_pressure
        self.parameters["diastolic_pressure"] = diastolic_pressure
        self.parameters["temperature"] = temperature
        self.parameters["weight"] = weight
        self.parameters["height"] = height
        self.parameters["sp_o2"] = sp_o2


    def get_parameters(self):
        return self.parameters

    def bmi(self):
       height_in_meters = self.parameters["height"] / 100
       return self.parameters["weight"] / (height_in_meters ** 2)

    def add_symptoms(self,symptom):
        self.parameters["symptoms"].append(symptom)







