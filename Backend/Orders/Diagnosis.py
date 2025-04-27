from Backend.Tests.hematology import BloodTest

#First analyze Blood Morphology

class Morphology:
    def __init__(self, blood_results: dict, gender: str):
        self.blood_result = blood_results
        self.gender = gender

    def analyze_RBC(self):  # mln/µl
        rbc_value = self.blood_result[BloodTest.RBC.value]
        if rbc_value is None:
            return "No RBC result available."

        if self.gender == "Female":
            if 3.5 < rbc_value < 5.2:
                return "Normal"
            elif rbc_value <= 3.5:
                return "Too low number of RBC"
            else:
                return "Too high number of RBC"
        elif self.gender == "Male":
            if 4.2 < rbc_value < 5.4:
                return "Normal"
            elif rbc_value <= 4.2:
                return "Too low number of RBC"
            else:
                return "Too high number of RBC"
        else:
            return "Unknown gender"





