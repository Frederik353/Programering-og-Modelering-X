

# oppgave a
"""
from microbit import *
import radio


radio.on()
radio.config(channel = 3)

while True:

    if button_a.was_pressed():
        radio.send("hei")
    incoming = radio.receive()
    if incoming:
        display.show(incoming)
        dispaly.clear()
        sleep(1000)
"""
# oppgave b
"""
from microbit import *
import radio


radio.on()
radio.config(channel = 3)

count = 0
while True:
    if button_a.was_pressed():
        radio.send(count)
        count += 1
    incoming = radio.receive()
    if incoming:
        display.show(incoming)
        dispaly.clear()
        sleep(1000)
"""


# oppgave c


from microbit import *
import radio

radio.on()
radio.config(channel = 3)
# compass.calibrate()

# directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
directions = ["N", "E", "S", "W"]

while True:
    degrees = str(compass.heading())
    radio.send(degrees)

    incoming = radio.receive()
    if incoming:
        incoming = int(incoming)
        incoming = round(incoming / (360. / len(directions)))
        display.show(directions[incoming % len(directions)])