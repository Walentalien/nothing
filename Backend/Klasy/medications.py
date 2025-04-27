from enum import Enum

from enum import Enum

class Medication(Enum):
    # Antybiotyki
    PENICILLIN = "Penicillin"
    AMOXICILLIN = "Amoxicillin"
    CIPROFLOXACIN = "Ciprofloxacin"
    DOXYCYCLINE = "Doxycycline"
    LEVOFLOXACIN = "Levofloxacin"
    CLINDAMYCIN = "Clindamycin"
    AZITHROMYCIN = "Azithromycin"
    MEROPENEM = "Meropenem"
    VANCOMYCIN = "Vancomycin"
    ERYTHROMYCIN = "Erythromycin"
    METRONIDAZOLE = "Metronidazole"

    # Leki przeciwbólowe
    PARACETAMOL = "Paracetamol"
    IBUPROFEN = "Ibuprofen"
    ASPIRIN = "Aspirin"
    NAPROXEN = "Naproxen"
    DICLOFENAC = "Diclofenac"
    COXIBS = "Coxibs"
    TRAMADOL = "Tramadol"
    OXYCODONE = "Oxycodone"
    CODEINE = "Codeine"

    # Leki przeciwgorączkowe
    ACETAMINOPHEN = "Acetaminophen"
    IBUPROFEN_FEVER = "Ibuprofen (for fever)"
    ASPIRIN_FEVER = "Aspirin (for fever)"

    # Leki przeciwzapalne
    PREDNISOLONE = "Prednisolone"
    HYDROCORTISONE = "Hydrocortisone"
    BETAMETHASONE = "Betamethasone"
    METHYLPREDNISOLONE = "Methylprednisolone"

    # Leki przeciwhistaminowe
    DIPHENHYDRAMINE = "Diphenhydramine"
    LORATADINE = "Loratadine"
    CETIRIZINE = "Cetirizine"
    FEXOFENADINE = "Fexofenadine"

    # Leki przeciwcukrzycowe
    METFORMIN = "Metformin"
    INSULIN = "Insulin"
    GLYBURIDE = "Glyburide"
    SGLT2_INHIBITOR = "SGLT2 Inhibitor"
    LIRAGLUTIDE = "Liraglutide"

    # Leki przeciwdepresyjne
    FLUOXETINE = "Fluoxetine"
    SERTRALINE = "Sertraline"
    CITALOPRAM = "Citalopram"
    ESCITALOPRAM = "Escitalopram"
    PAROXETINE = "Paroxetine"
    BUPROPION = "Bupropion"

    # Leki przeciwnadciśnieniowe
    LOSARTAN = "Losartan"
    AMLODIPINE = "Amlodipine"
    ENALAPRIL = "Enalapril"
    METOPROLOL = "Metoprolol"
    LISINOPRIL = "Lisinopril"
    HYDROCHLOROTHIAZIDE = "Hydrochlorothiazide"

    # Leki na choroby serca
    ASPIRIN_CARDIO = "Aspirin Cardio"
    ATORVASTATIN = "Atorvastatin"
    SIMVASTATIN = "Simvastatin"
    RAMIPRIL = "Ramipril"
    DILTIAZEM = "Diltiazem"

    # Leki przeciwzakrzepowe
    WARFARIN = "Warfarin"
    RIVAROXABAN = "Rivaroxaban"
    APIXABAN = "Apixaban"
    DALTEPARIN = "Dalteparin"
    ENOXAPARIN = "Enoxaparin"

    # Leki immunosupresyjne
    TACROLIMUS = "Tacrolimus"
    CYCLOSPORINE = "Cyclosporine"
    MYCOPHENOLATE = "Mycophenolate"
    AZATHIOPRINE = "Azathioprine"

    # Leki przeciwgrzybicze
    FLUCONAZOLE = "Fluconazole"
    ITRACONAZOLE = "Itraconazole"
    KETOCONAZOLE = "Ketoconazole"
    AMPHOTERICIN_B = "Amphotericin B"

    # Leki przeciwwirusowe
    ACYCLOVIR = "Acyclovir"
    OSeltamivir = "Oseltamivir"
    REMDESIVIR = "Remdesivir"
    ZIDOVUDINE = "Zidovudine"

    # Leki na astmę i alergie
    SALBUTAMOL = "Salbutamol"
    BUDESONIDE = "Budesonide"
    FLUTICASONE = "Fluticasone"
    MONTELUKAST = "Montelukast"
    THEOPHYLLINE = "Theophylline"

    # Leki przeciwpsychotyczne
    CLOZAPINE = "Clozapine"
    RISPERIDONE = "Risperidone"
    OLANZAPINE = "Olanzapine"
    QUETIAPINE = "Quetiapine"
    ARIPIPRAZOLE = "Aripiprazole"

    # Leki przeciwdrgawkowe
    PHENYTOIN = "Phenytoin"
    CARBAMAZEPINE = "Carbamazepine"
    VALPROATE = "Valproate"
    LAMOTRIGINE = "Lamotrigine"

    # Leki na choroby tarczycy
    LEVOTHYROXINE = "Levothyroxine"
    METHIMAZOLE = "Methimazole"
    PROPYLTHIOURACIL = "Propylthiouracil"

    # Leki uspokajające i nasenne
    DIAZEPAM = "Diazepam"
    LORAZEPAM = "Lorazepam"
    ALPRAZOLAM = "Alprazolam"
    TEMAZEPAM = "Temazepam"

    # Leki na depresję
    AMITRYPTYLINE = "Amitriptyline"
    NORTRIPTYLINE = "Nortriptyline"
    DULOXETINE = "Duloxetine"
    VENLAFAXINE = "Venlafaxine"

    # Leki hormonalne
    ESTRADIOL = "Estradiol"
    TESTOSTERONE = "Testosterone"
    PROGESTERONE = "Progesterone"
    MEDROXYPROGESTERONE = "Medroxyprogesterone"

    # Leki przeciwwirusowe
    LAMIVUDINE = "Lamivudine"
    FAVIPIRAVIR = "Favipiravir"
    LOPINAVIR = "Lopinavir"
    RITONAVIR = "Ritonavir"

    # Leki na choroby Parkinsona
    LEVODOPA = "Levodopa"
    BENZTROPINE = "Benztropine"
    PRAMIPEXOLE = "Pramipexole"
    ROPINIROLE = "Ropinirole"

    # Leki na choroby żołądka
    OMEPRAZOLE = "Omeprazole"
    ESOMEPRAZOLE = "Esomeprazole"
    RANITIDINE = "Ranitidine"
    FAMOTIDINE = "Famotidine"

    # Leki na choroby wątroby
    URSODEOXYCHOLIC_ACID = "Ursodeoxycholic acid"
    LIVER_SUPPORT = "Liver Support"

