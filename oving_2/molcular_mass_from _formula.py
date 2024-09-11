import csv
import unittest


def csv_search(element):
    with open("./øving 2/periodic_table.csv",  mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["Symbol"] == element:
                return row


def insert_string(string, index, insert):

    return string[:index] + insert + string[index:]


def molarmasse(formel):
    index_offset = 0  # for loop sjekker kun formel verdi en gang og trenger derfor en offset for å korrigere for at vi setter in f.eks + tegn
    # hvis stor bokstav = nytt element, legg til + tegn hvis tall gange
    for index, letter in enumerate(formel):
        # print(formel)
        if letter.isupper() or letter == "(":
            formel = insert_string(formel, index + index_offset, "+")
            index_offset += 1

        elif letter.isnumeric() and not formel[index + index_offset - 1].isnumeric():
            formel = insert_string(formel, index + index_offset, "*")
            # gjentat siden vil ikke offsette hvis bokstaven er liten og man ikke setter in noe
            index_offset += 1

    index_offset = 0
    for index, letter in enumerate(formel):
        if letter.isupper():
            element = letter + (formel[index + index_offset + 1]
                                if formel[index + index_offset + 1].islower() else "")

            element_info = csv_search(element)

            formel = formel.replace(element, element_info["AtomicMass"], 1)
            index_offset += len(element_info["AtomicMass"]) - len(element)

    return eval(formel)


class test_masse(unittest.TestCase):
    def test_masse_til_molekyl(self):
        self.assertEqual(round(molarmasse("O2")),
                         round(31.9988), "O2 / Oksygen")
        self.assertEqual(round(molarmasse("CO2")),
                         round(44.0095), "CO2 / Karbondioksid")
        self.assertEqual(round(molarmasse("H2")),
                         round(2.01588), "H2 / Dihydrogen")
        self.assertEqual(round(molarmasse("C6H12O6")),
                         round(180.15588), "C6H12O6 / Glukose")
        self.assertEqual(round(molarmasse("H2SO4")),
                         round(98.07848), "H2SO4  / Svovelsyre")
        self.assertEqual(round(molarmasse("Mg(OH)2")), round(
            58.31968), "Mg(OH)2 / Magnesiumhydroxid")
        self.assertEqual(round(molarmasse("C3H5(OH)3")),
                         round(92.09382), "C3H5(OH)3 / Glyserol")
        self.assertEqual(round(molarmasse("Al(NO3)3")), round(
            212.996238), "Al(NO3)3 / Aluminiumnitrat")
        self.assertEqual(round(molarmasse("(CH3COO)2Ca")), round(
            158.16604), "(CH3COO)2Ca / Kalciumacetat")


if __name__ == "__main__":
    formel = "C3H5(OH)3"
    print(formel)
    print(f"molekylet {formel} har en masse på {molarmasse(formel)} g/mol")

    unittest.main()
