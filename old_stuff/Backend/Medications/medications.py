from enum import Enum

from enum import Enum

class MedicationType(Enum):
    # Kardiologiczne
    BETA_BLOCKER = "beta-blocker"
    ACE_INHIBITOR = "ace-inhibitor"
    CALCIUM_CHANNEL_BLOCKER = "calcium-channel-blocker"
    VASOPRESSOR = "vasopressor"
    DIURETIC = "diuretic"
    STATIN = "statin"
    NITRATES = "nitrates"

    # Przeciwbólowe i przeciwzapalne
    PARACETAMOL = "paracetamol"
    NSAID = "non-steroidal anti-inflammatory drug"
    OPIOID = "opioid"
    COX2_INHIBITOR = "cox-2 inhibitor"

    # Endokrynologiczne / metaboliczne
    STEROID = "steroid"
    INSULIN = "insulin"
    METFORMIN = "metformin"
    THYROXINE = "thyroxine"

    # Antybiotyki i przeciwinfekcyjne
    PENICILLIN = "penicillin"
    MACROLIDE = "macrolide"
    FLUOROQUINOLONE = "fluoroquinolone"
    TETRACYCLINE = "tetracycline"
    ANTIVIRAL = "antiviral"
    ANTIFUNGAL = "antifungal"

    # Psychiatryczne / neurologiczne
    SSRI = "ssri"
    BENZODIAZEPINE = "benzodiazepine"
    ANTIPSYCHOTIC = "antipsychotic"
    ANTIEPILEPTIC = "antiepileptic"

    # Inne
    ANTICOAGULANT = "anticoagulant"
    ANTIPLATELET = "antiplatelet"
    PROTON_PUMP_INHIBITOR = "proton-pump inhibitor"
    ANTIHISTAMINE = "antihistamine"
    BRONCHODILATOR = "bronchodilator"
    IMMUNOSUPPRESSANT = "immunosuppressant"
    VITAMIN_D = "vitamin D"
    IRON_SUPPLEMENT = "iron supplement"
    ORAL_CONTRACEPTIVE = "oral contraceptive"