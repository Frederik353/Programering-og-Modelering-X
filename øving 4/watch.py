# "0", "en" og "pin 2"

# oppgave a
"""
from microbit import *

while True:
    if pin0.read_digital():
        display.scroll("0")
    elif pin1.read_digital():
        display.scroll("en")
    elif pin2.read_digital():
        display.scroll("pin 2")
    else:
        display.show(Image.SAD)
"""


# oppgave b



from microbit import *
import time

images = [Image.CLOCK9, Image.CLOCK8, Image.CLOCK7, Image.CLOCK6, Image.CLOCK5, Image.CLOCK4, Image.CLOCK3, Image.CLOCK2, Image.CLOCK1, Image.CLOCK12, Image.CLOCK11, Image.CLOCK10]

def dim(image, dimness):
    new_image = Image(5,5)
    dimnessLevels = [1,3,5,7,9]
    for y in range(5):
        for x in range(5):
            if image.get_pixel(x,y) > 0:
                new_image.set_pixel(y,x,dimnessLevels[dimness])
            else: new_image.set_pixel(y,x,0)
    return new_image

while True:
    for i in range(0,5):
        for j in range(0,12):
            display.show(dim(images[j], i))

            start = time.ticks_ms()
            while(time.ticks_diff(time.ticks_ms(), start) < 1000 ):
                if button_a.is_pressed():
                    display.show(Image.HAPPY)
                elif button_b.is_pressed():
                    display.show(Image.SAD)


# oppgave c

"""
from microbit import *

letters = [Image(
                "9999:"
                "9000:"
                "9999:"
                "9000:"
                "9000"),
                Image(
                "00000:"
                "09990:"
                "90000:"
                "90000:"
                "90000"),
                Image(
                "09990:"
                "90009:"
                "99990:"
                "9000:"
                "09990"),
                Image(
                "00009:"
                "00009:"
                "09999:"
                "90009:"
                "09999"),
                Image(
                "09990:"
                "90009:"
                "99990:"
                "9000:"
                "09990"),
                Image(
                "00000:"
                "09990:"
                "90000:"
                "90000:"
                "90000"),
                Image(
                "00900:"
                "00000:"
                "00900:"
                "00900:"
                "00900"),
                Image(
                "90000:"
                "90900:"
                "99000:"
                "90090:"
                "90009"),
            ]


while True:
    # display.scroll("Frederik")
    for i in letters:
        display.show(i)
        sleep(750)

"""