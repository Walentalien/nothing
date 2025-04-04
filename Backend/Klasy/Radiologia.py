class BadanieRadiologiczne:
    def __init__(self, nazwa, opis=None, wynik=None):
        self.nazwa = nazwa
        self.opis = opis
        self._wynik = wynik

    def dodaj_wynik(self, wynik):
        self._wynik = wynik

    def dodaj_opis(self,opis):
        self.opis = opis
