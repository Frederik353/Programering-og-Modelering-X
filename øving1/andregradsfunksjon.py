

import math # siden math libraryen delvis kjører i C språket som er mye raskere en python vil math.sqrt være  mere effektiv og raskere enn å opphøye i 0.5 (**0.5)



a = int(input("koeffisient a: "))
b = int(input("koeffisient b: "))
c = int(input("koeffisient c: "))

d = b**2-4*a*c  # ting under kvadratroten

if d < 0:
    print ("ingen rasjonal løsning")
elif d == 0:
    x = ( - b + math.sqrt( b**2 - 4 * a * c)) / 2 * a
    print (f"lingningen har en løsning x = {x}")
else:
    x1 = ( - b + math.sqrt( b**2 - 4 * a * c)) / 2 * a
    x2 = ( - b - math.sqrt( b**2 - 4 * a * c)) / 2 * a
    print (f"lingningen har to løsninger x1 = {x1} og x2 = {x2}")
