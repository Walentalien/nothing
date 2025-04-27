from enum import Enum


class UrineTest(Enum):
    PH = "pH"
    PROTEIN = "Protein"
    GLUCOSE = "Glucose"
    LEUKOCYTES = "Leukocytes"
    NITRITES = "Nitrites"
    UROBILINOGEN = "Urobilinogen"
    BLOOD = "Blood"
    KETONES = "Ketones"
    BILIRUBIN = "Bilirubin"




class UrineAnalysis:
    def __init__(self):
        self.tests = { test: None for test in UrineTest}

    def add_urine_test(self, test: UrineTest, result):
        self.tests[test] = result

