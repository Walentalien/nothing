from Spec import Specjalizacja

class Pacjent:
    def __init__(self, imie,wiek,plec, puls = None, cisnienie = None):
        self.imie = imie
        self.wiek = wiek
        self.plec = plec
        self.puls = puls
        self.cisnienie = cisnienie
        self.reszta = []   #dodawanie innych parametórw, w trakcie rozbudowy



class Doktor:
    def __init__(self, imie, specjalizacja: Specjalizacja):
        self.imie = imie
        self.specjalizacja = specjalizacja








