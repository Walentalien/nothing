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

    def analyze_HGB(self):  # Hemoglobina g/dl
        hgb_value = self.blood_result[BloodTest.HGB.value]
        if hgb_value is None:
            return "No HGB result available."
        if self.gender == "Female":
            if 12.0 <= hgb_value <= 16.0:
                return "Normal"
            elif hgb_value < 12.0:
                return "Too low hemoglobin"
            else:
                return "Too high hemoglobin"
        elif self.gender == "Male":
            if 13.5 <= hgb_value <= 17.5:
                return "Normal"
            elif hgb_value < 13.5:
                return "Too low hemoglobin"
            else:
                return "Too high hemoglobin"
        else:
            return "Unknown gender"

    def analyze_HCT(self):  # Hematokryt %
        hct_value = self.blood_result[BloodTest.HCT.value]
        if hct_value is None:
            return "No HCT result available."

        if self.gender == "Female":
            if 36.0 <= hct_value <= 46.0:
                return "Normal"
            elif hct_value < 36.0:
                return "Too low hematocrit"
            else:
                return "Too high hematocrit"
        elif self.gender == "Male":
            if 40.0 <= hct_value <= 52.0:
                return "Normal"
            elif hct_value < 40.0:
                return "Too low hematocrit"
            else:
                return "Too high hematocrit"
        else:
            return "Unknown gender"

    def analyze_WBC(self):  # Leukocyty (tys./µl)
        wbc_value = self.blood_result[BloodTest.WBC.value]
        if wbc_value is None:
            return "No WBC result available."

        if 4.0 <= wbc_value <= 10.0:
            return "Normal"
        elif wbc_value < 4.0:
            return "Leukopenia (Too low)"
        else:
            return "Leukocytosis (Too high)"

    def analyze_PLT(self):  # Płytki krwi tys./µl
        plt_value = self.blood_result[BloodTest.PLT.value]
        if plt_value is None:
            return "No PLT result available."

        if 150 <= plt_value <= 400:
            return "Normal"
        elif plt_value < 150:
            return "Thrombocytopenia (Too low)"
        else:
            return "Thrombocytosis (Too high)"

    def analyze_MCV(self):  # Średnia objętość krwinki czerwonej (fL)
        mcv_value = self.blood_result[BloodTest.MCV.value]
        if mcv_value is None:
            return "No MCV result available."

        if 80 <= mcv_value <= 100:
            return "Normal"
        elif mcv_value < 80:
            return "Microcytosis (Too low)"
        else:
            return "Macrocytosis (Too high)"

    def analyze_MCH(self):  # Średnia masa hemoglobiny w krwince (pg)
        mch_value = self.blood_result[BloodTest.MCH.value]
        if mch_value is None:
            return "No MCH result available."

        if 27 <= mch_value <= 33:
            return "Normal"
        elif mch_value < 27:
            return "Hypochromia (Too low)"
        else:
            return "Too high MCH"

    def analyze_MCHC(self):  # Średnie stężenie hemoglobiny w krwince (%)
        mchc_value = self.blood_result[BloodTest.MCHC.value]
        if mchc_value is None:
            return "No MCHC result available."

        if 32 <= mchc_value <= 36:
            return "Normal"
        elif mchc_value < 32:
            return "Too low MCHC"
        else:
            return "Too high MCHC"








