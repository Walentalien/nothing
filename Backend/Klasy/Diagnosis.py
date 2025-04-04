import os
import random
from tkinter import Image


# nadcisnienie
#  0 - norma
#  1 - przedciśnieniowy
#  2 - nadciśnienie stopnia 1
#  3 - nadciśnienie stopnia 2
#  4 - natychmiastowa interwencja


def czy_nadcisnienie(cisnienie_skurczowe, cisnienie_rozkurczowe):
    try:
        cisnienie_skurczowe = float(cisnienie_skurczowe)
        cisnienie_rozkurczowe = float(cisnienie_rozkurczowe)
    except ValueError:
        return "Błąd: Podaj liczby.", -1
    if cisnienie_skurczowe < 120 and cisnienie_rozkurczowe < 80:
        return "Prawidłowe ciśnienie krwi", 0
    elif 120 <= cisnienie_skurczowe < 130 and cisnienie_rozkurczowe < 80:
        return "Stan przednadciśnieniowy", 1
    elif 130 <= cisnienie_skurczowe < 140 or 80 <= cisnienie_rozkurczowe < 90:
        return "Nadciśnienie stopnia 1", 2
    elif 140 <= cisnienie_skurczowe or 90 <= cisnienie_rozkurczowe:
        return "Nadciśnienie stopnia 2", 3
    elif cisnienie_skurczowe > 200 or cisnienie_rozkurczowe > 140:
        return "Przełom nadciśnieniowy – wymaga natychmiastowej interwencji medycznej", 4
    else:
        return "Nieprawidłowe wartości ciśnienia krwi", -1



#Morfologia

class Morfologia:
    def __init__(self, RBC, WBC, Hb, HCT, platelets, pacjent):
        self.RBC = RBC
        self.WBC = WBC
        self.Hb = Hb
        self.HCT = HCT
        self.platelets = platelets

#analiza czerwonych krwinek

    def analiza_RBC(self):
        if self.RBC < 4.7:
            return "Rozważ Anemie", 0
        elif self.RBC > 6.1:
            return "Rozważ Policytmie, na co jeszcze warto popatrzeć", 1
        else:
            return "Prawidłowa liczba czerwonych krwinek", 2

#analiza białych krwinek
    def analiza_WBC(self):
        if self.WBC < 4.0:
            return "Rozważ Leukopenie", 0
        elif self.WBC > 11.0:
            return "Rozważ infekcje, na co warto popatrzeć?", 1
        else:
            return "Prawidłowa liczba białych krwinek", 2

#analiza hemoglobiny
    def analiza_Hb(self):

        if self.Hb < 12.0:
            return "możliwa anemia, dlaczego? ", 0
        elif self.Hb > 18.0:
            return "Hemoglobinemia, dlaczego?", 1
        else:
            return "Prawidłowy poziom hemoglobiny", 2
#analiza hematokrytu

    def analiza_HCT(self):
        if self.HCT < 37:
            return "Niski hematokryt (możliwa anemia)", 0
        elif self.HCT > 54:
            return "Wysoki hematokryt (możliwa policytemia)", 1
        else:
            return "Prawidłowy hematokryt", 2
#analiza płytek krwi

    def analiza_platelets(self):
        if self.platelets < 150:
            return "Tromboctopenia - na co jeszcze warto zwrócić uwage?, APPT/PT?"
        elif self.platelets > 450:
            return "Trombozytoza"
        else:
            return "Prawidłowa liczba płytek krwi"


# Klasa do funkcji wątrobowych
class FunkcjeWatrobowe:
    def __init__(self, alt, ast, alp, bilirubina, ggtp, albuminy):
        self.alt = alt
        self.ast = ast
        self.bilirubina = bilirubina
        self.ggtp = ggtp
        self.albuminy = albuminy

    def ocen_alt(self):
        if self.alt <= 40:
            return "ALT w normie", 0
        return f"Podwyższone ALT: {self.alt} U/L", 1

    def ocen_ast(self):
        if self.ast <= 40:
            return "AST w normie"
        return f"Podwyższone AST: {self.ast} U/L",2


    def ocen_bilirubine(self):
        if self.bilirubina <= 1.2:
            return "Bilirubina w normie"
        return f"Podwyższona bilirubina: {self.bilirubina} mg/dL",3

    def ocen_ggtp(self):
        if self.ggtp <= 60:
            return "GGTP w normie"
        return f"Podwyższone GGTP: {self.ggtp} U/L",4

    def ocen_albuminy(self):
        if 3.4 <= self.albuminy <= 5.4:
            return "Albuminy w normie"
        return f"Nieprawidłowy poziom albumin: {self.albuminy} g/dL",5





# --------------- Mocz ---------------------------
class AnalizaMoczu:
    def __init__(self, kolor, przejrzystosc, ph, bialko, glukoza):
        self.kolor = kolor
        self.przejrzystosc = przejrzystosc
        self.ph = ph
        self.bialko = bialko
        self.glukoza = glukoza

    def a_kolor(self):
        if self.kolor in ["słomkowy", "żółty", "jasnożółty"]:
            return "Prawidłowy kolor moczu"
        return f"Nieprawidłowy kolor moczu: {self.kolor}"

    def a_przejrzystosc(self):
        return self.przejrzystosc == "przejrzysty"

    def a_ph(self):
        print("Czy ph w normie")
        if isinstance(self.ph, (int, float)) and 6.5 <= self.ph <= 7.5:
            return True
        return False

    def a_bialko(self):
        if self.bialko in ["ujemne", "brak"]:
            return True #  nie mamy białka
        return False

    def a_glukoze(self):
        if self.glukoza in ["ujemna", "brak"]:
            return True
        return False


class EKG:
    def __init__(self, data, wynik, plik_ekg):
        self.data = data
        self.__wynik = wynik
        self.plik_ekg = plik_ekg
        #w zależnośći  od dostępnych EKG -- będziemy zwiększac liczbe typ_rytmu
        self.typy_rytmu = {
            "rytm zatokowy",
            "zatokowa tachykardia",
            "zatokowa bradykardia",
            "migotanie przedsionków",
            "trzepotanie przedsionków",
            "częstoskurcz komorowy",
            "blok przedsionkowo-komorowy",
            "asystolia",
            "zaburzenia rytmu"
            "Blok Mobitz I",
            "Blok Mobitz II",
            "Blok Mobitz III",
        }
    def pokaz_ekg(self):
        if os.path.exists(self.plik_ekg):
            img = Image.open(self.plik_ekg)
            img.show()
        else:
            print(f"Plik {self.plik_ekg} nie istnieje.")





# Objawy



# Badania dodatkowe

def zapytaj_dodatkowe_badania():
    print("Jakie dodatkowe badania chciałbyś zlecić?\n")
    print("Wpisz kolejne badania (np. 'Morfologia', 'USG jamy brzusznej').")
    print("Wpisz 'koniec', aby zakończyć.")

    badania = []






