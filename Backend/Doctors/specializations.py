from enum import Enum

# name: value
class Specializations(Enum):
    CARDIOLOGY = "Cardiology"
    NEUROLOGY = "Neurology"
    ORTHOPEDICS = "Orthopedics"
    PEDIATRICS = "Pediatrics"
    DERMATOLOGY = "Dermatology"
    SURGEON = "Surgeon"
    GASTROENTEROLOGIST = "Gastroenterologist"
    PSYCHIATRY = "Psychiatry"
    OPHTHALMOLOGY = "Ophthalmology"
    ENDOCRINOLOGY = "Endocrinology"
    PULMONOLOGY = "Pulmonology"
    RADIOLOGY = "Radiology"


class Level(Enum):
    STUDENT = "Student"
    INTERN = "Intern"
    RESIDENT = "Resident"
    SPECIALIST = "Specialist"

#More specializations/Levels can be added during the app build process







