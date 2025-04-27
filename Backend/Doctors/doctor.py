from specializations import Specializations, Level


class Doctor:
    def __init__(self,name, spec: Specializations, lev: Level):
        self.name = name
        self.specialization = spec
        self.level = lev

    def change_specialization(self, new_specialization):
        self.specialization = new_specialization

    def change_level(self, new_level):
        self.level = new_level












