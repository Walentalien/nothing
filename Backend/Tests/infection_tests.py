from enum import Enum

class InfectionDiagnostics(Enum):
    PROCALCITONIN = "Procalcitonin"
    EBV_IGG = "EBV IgG"
    EBV_IGM = "EBV IgM"
    TOXOPLASMA_IGG = "Toxoplasma IgG"
    TOXOPLASMA_IGM = "Toxoplasma IgM"
    BORRELIA_IGG = "Borrelia IgG"
    BORRELIA_IGM = "Borrelia IgM"
    HBS_ANTIGEN = "HBs Antigen"  #
    HBS_ANTIBODIES = "HBs Antibodies"
    HCV_ANTIBODIES = "HCV Antibodies"
    HELICOBACTER_PYLORI_IGG = "Helicobacter pylori IgG"
    MYCOPLASMA_PNEUMONIAE_IGG = "Mycoplasma pneumoniae IgG"
    MYCOPLASMA_PNEUMONIAE_IGM = "Mycoplasma pneumoniae IgM"
    PERTUSSIS_IGG = "Pertussis IgG"
    PERTUSSIS_IGM = "Pertussis IgM"
    PERTUSSIS_IGA = "Pertussis IgA"