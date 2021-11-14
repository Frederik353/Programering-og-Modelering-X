





ønsket_volum = float(input("sluttvolum (ml): "))
opprinnelig_konsentrasjon = float(input("opprinnelig konsentrasjon (M): "))
ønsket_konsentrasjon = float(input("ønsket konsentrasjon (M): "))


#C1V1 = C2V2
nødvendig_volum = (ønsket_konsentrasjon * ønsket_volum) / opprinnelig_konsentrasjon
print(f"volum: {nødvendig_volum} ml")
