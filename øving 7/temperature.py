

class Temperature:
    """ Get temperature from xC, or xK, or xF value, where value is Celsius, Kelvin or Fahrenheit"""

    def __init__(self, value):
        self.value = value
        self.celsius = None
        self.kelvin = None
        self.fahrenheit = None
        try:
            if value[-1].upper() in ['C', 'F', 'K']:
                self.value = value.upper()
            else:
                raise ValueError('Temperature must be C|F|K')
        except ValueError as e:
            print("Value error, Jim.", e)
        if self.value[-1] is "C":
            self._celsius()
        elif self.value[-1] is "F":
            self._fahrenheit()
        elif self.value[-1] is "K":
            self._kelvin()

    def _celsius(self):
        self.celsius = round((float(self.value[:-1])),2)
        self.fahrenheit = round(((float(self.value[:-1])* 9 / 5) + 32),2)
        self.kelvin = round((float(self.value[:-1]) + 273.15),2)
        print("It's Celsius, Jim. T:", end=" ")

    def _fahrenheit(self):
        self.fahrenheit = round((float(self.value[:-1])),2)
        self.celsius = round((((float(self.value[:-1]) - 32) * 5/9)),4)
        self.kelvin = round((self.celsius + 273.15),3)
        print("It's Fahrenheit, Jim  T:", end=" ")

    def _kelvin(self):
        self.kelvin = round((float(self.value[:-1])),2)
        self.celsius = round((float(self.value[:-1]) - 273.15),2)
        self.fahrenheit = round(((self.celsius * 9 / 5) + 32),2)
        print("It's Kelvin, Jim T:", end=" ")

t = Temperature("0F")
print(t.value)
print(str(t.celsius)+"C", str(t.kelvin)+"K", str(t.fahrenheit)+"F")

