class BadanieRadiologiczne:
    def __init__(self, nazwa, opis=None, wynik=None):
        self.nazwa = nazwa
        self.opis = opis
        self.wynik = wynik

    def dodaj_wynik(self, wynik):
        self.wynik = wynik

    def dodaj_opis(self,opis):
        self.opis = opis
