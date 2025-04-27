
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

    def a_alt(self):
        if self.alt <= 40:
            return "ALT w normie", 0
        return "ALT podwyższone", 1

    def a_ast(self):
        if self.ast <= 40:
            return "AST w normie" ,0
        return "AST podwyższone",1

    def a_bilirubine(self):
        if self.bilirubina <= 1.2:
            return "Bilirubina w normie", 0
        return "Podwyższona Bilirubina",1

    def a_ggtp(self):
        if self.ggtp <= 60:
            return "GGTP w normie",0
        return "Podwyszona GGTP", 1

    def a_albuminy(self):
        if 3.4 <= self.albuminy <= 5.4:
            return "Albuminy w normie", o
        elif self.albuminy > 5.4:
            "hiperalbuminemia", 1
        else:
            "hipoalbuminemia", 2






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
            return "Prawidłowy kolor moczu", 0
        return "Nieprawidłowy kolor moczu", 1

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
        self.wynik = wynik
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






