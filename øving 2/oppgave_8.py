import csv
import re


formula = "C3H5(OH)3"
# formula = "C6H12O6"
# formula = "C2H5Br6C6H12Al6 "
# formula = " C77H120N18O26S " # endorfin
# formula = str(input("molekylformel: "))

print(formula)



def csv_search(element):
    with open("C:/Users/frede/Desktop/Programering-og-Modelering-X/øving 2/periodic_table.csv",  mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["Symbol"] == element:
                return row




def masse_til_molekyl(formula):


    index_offset = 0 # for loop sjekker kun formula verdi en gang og trenger derfor en offset for å korrigere for at vi setter in f.eks + tegn
    for index, letter in enumerate(formula): # hvis stor bokstav = nytt element, legg til + tegn hvis tall gange
        if letter.isupper() or letter == "(":
            formula = formula[:index + index_offset] + "+" + formula[index + index_offset:]

            index_offset += 1
        elif letter.isnumeric() and not formula[index + index_offset - 1].isnumeric():
            formula = formula[:index + index_offset] + "*" + formula[index + index_offset:]
            index_offset += 1 #gjentat siden vil ikke offsette hvis bokstaven er liten og man ikke setter in noe


    index_offset = 0
    for index, letter in enumerate(formula):
        if letter.isupper():
            element = letter + (formula[index + index_offset + 1] if formula[index + index_offset + 1].islower() else "")

            element_info = csv_search(element)

            formula = formula.replace(element, element_info["AtomicMass"], 1)
            index_offset += len(element_info["AtomicMass"]) - len(element)

    return formula

print(f"molekylet {formula} har en masse på {eval( masse_til_molekyl(formula) )} g/mol")


def csv_search(element):
    with open("C:/Users/frede/Desktop/Programering-og-Modelering-X/øving 2/periodic_table.csv",  mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            print(row["AtomicMass"])
