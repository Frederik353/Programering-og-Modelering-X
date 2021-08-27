import math

# numpy har en funksjon for dette som er raskere np.linalg.norm([3,4])


a = [5,3]
b = [12,7]

lengder = [abs(a[0] - b[0]),abs(a[1] - b[1])] # x, y retning

vektorlengde = math.sqrt(lengder[0]**2 + lengder[1]**2)

print(lengder, vektorlengde)















