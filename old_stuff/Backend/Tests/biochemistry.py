from enum import Enum
class BiochemistryTests(Enum):
    ALT = "Alt"
    AST = "Ast"
    GLUCOSE = "Glucose"
    CHOLESTEROL = "Cholesterol"
    TRIGLYCERIDES = "Triglycerides"
    CREATININE = "Creatinine"
    BILIRUBIN = "Bilirubin"
    ALBUMIN = "Albumin"
    CRP = "Crp"
    GGTP = "Ggtp"
    SODIUM = "Sodium"
    POTASSIUM = "Potassium"
    IONIZED_CALCIUM = "Ionized Calcium"
    URIC_ACID = "Uric Acid"
    FERRITIN = "Ferritin"
    VITAMIN_B12 = "Vitamin B12"
    FOLIC_ACID = "Folic Acid"
    TRANSFERRIN = "Transferrin"
    TOTAL_CALCIUM = "Total Calcium"
    IGA = "IgA"
    IGM = "IgM"
    IGG = "IgG"
    VITAMIN_D = "Vitamin D"



    
class Biochemistry:
    def __init__(self):
        self.test_ordered = []

    def add_test(self, test: BiochemistryTests):
        self.test_ordered.append(test)
    def remove_test(self, test: BiochemistryTests):
        if test in self.test_ordered:
            self.test_ordered.remove(test)
    def show_tests(self):
        if self.test_ordered:
            for test in self.test_ordered:
                print(test)
        else:
            print("no tests")



