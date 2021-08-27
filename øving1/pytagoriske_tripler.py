
import math

a = int(input("koeffisient a: "))
b = int(input("koeffisient b: "))
c = int(input("koeffisient c: "))


array = [a,b,c]
array.sort()

if array[0]**2 + array[1]**2 == array[2]**2:
    print(f"{a,b,c} er en pytagorisk trippel")
else:
    print(f"{a,b,c} er ikke en pytagorisk trippel")
