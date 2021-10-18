import csv
import unittest
import oppgave_5

# C3H5(OH)3


def csv_search(grunnstoff):
    with open("./øving 2/periodic_table.csv",  mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["Symbol"] == grunnstoff:
                return row

        raise Exception(f"fant ikke {grunnstoff} i listen, er du sikker på at du har skrevet inn formelen riktig?")


def molarmasse(formel):

    ny_formel = ""

    for index, value in enumerate(formel):
        if value.isalpha():
            if value.isupper():
                grunnstoff = value + (formel[index + 1] if formel[index + 1].islower() else "")
                grunnstoff_info = csv_search(grunnstoff)
                ny_formel +=  "+" + grunnstoff_info["AtomicMass"]
            continue

        elif value.isnumeric() and not formel[index - 1].isnumeric():
            ny_formel += "*"

        elif value == "(":
            ny_formel += "+"

        ny_formel += value

    return eval(ny_formel)


class test_masse(unittest.TestCase):
    def test_masse_til_molekyl(self):
        self.assertEqual(round(molarmasse("O2")), round(31.9988), "O2 / Oksygen")
        self.assertEqual(round(molarmasse("CO2")), round(44.0095), "CO2 / Karbondioksid")
        self.assertEqual(round(molarmasse("H2")), round(2.01588), "H2 / Dihydrogen")
        self.assertEqual(round(molarmasse("C6H12O6")), round(180.15588), "C6H12O6 / Glukose")
        self.assertEqual(round(molarmasse("H2SO4")), round(98.07848), "H2SO4  / Svovelsyre")
        self.assertEqual(round(molarmasse("Mg(OH)2")), round(58.31968), "Mg(OH)2 / Magnesiumhydroxid")
        self.assertEqual(round(molarmasse("C3H5(OH)3")), round(92.09382), "C3H5(OH)3 / Glyserol")
        self.assertEqual(round(molarmasse("Al(NO3)3")), round(212.996238), "Al(NO3)3 / Aluminiumnitrat")
        self.assertEqual(round(molarmasse("(CH3COO)2Ca")), round(158.16604), "(CH3COO)2Ca / Kalciumacetat")


if __name__ == "__main__":
    formel = "C3H5(OH)3"
    print(formel)
    print(f"molekylet {formel} har en masse på {molarmasse(formel)} g/mol")

    unittest.main()









































