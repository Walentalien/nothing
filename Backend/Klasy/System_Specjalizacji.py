from Spec import Specjalizacja


"""
Kardio -0 
rodzinna - 1
Chirurgia 2
Derma - 3 
Neuro - 4
Orto - 5
Pdychiatria - 6
Onkologia - 7
Pediatria - 7
Gineksy - 8
Endo - 9 
Alergologia - 10
Reumat-- 11

"""

class SystemSpecjalizacji:
    def __init__(self):
        self.specjalizacje = [
            Specjalizacja("Kardiologia"),
            Specjalizacja("Rodzinna"),
            Specjalizacja("Chirurgia"),
            Specjalizacja("Dermatologia"),
            Specjalizacja("Neurologia"),
            Specjalizacja("Ortopedia"),
            Specjalizacja("Psychiatria"),
            Specjalizacja("Onkologia"),
            Specjalizacja("Pediatria"),
            Specjalizacja("Ginekologia"),
            Specjalizacja("Endokrynologia"),
            Specjalizacja("Alergologia"),
            Specjalizacja("Urologia"),
            Specjalizacja("Reumatologia"),
        ]
    def wyswietl_specjalizacje(self):
        print("Wybierz specjalizację, która Cię interesuje:")

        try:
            wybor = int(input("Wprowadź numer specjalizacji: "))
            if wybor < 0 or wybor >= len(self.specjalizacje):
                print("Nieprawidłowy numer specjalizacji")
                return

            print("Na jakim etapie edukacji jesteś?\n")
            print("0 - Student, 1 - Stażysta, 2 - Rezydent, 3 - Specjalista")
            etap = int(input("Wprowadź numer etapu: "))

            poziomy = ["Student", "Stażysta", "Rezydent", "Specjalista"]
            if etap < 0 or etap > 3:
                print("Nieprawidłowy numer etapu")
                return

            self.specjalizacje[wybor].poziom = poziomy[etap]
        except ValueError:
            print("Wprowadź liczbę")
