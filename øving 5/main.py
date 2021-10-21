from microbit import *
import time
# import os


while True:
    logg = True 
    display.scroll ("Press A to start logging", delay = 75)
    time.sleep_ms(500)
    if button_a.was_pressed():
        writepath = "./temerature.txt"
        # mode = "a" if os.path.exists(writepath) else "w"
        mode = "w"
        with open(writepath, mode) as f:
            while logg:
                currentTemp = temperature()
                f.write(str(currentTemp) + "\n")
                print((currentTemp,))
                time.sleep_ms(500)
                display.clear()
                time.sleep_ms(500)
                display.show(Image.SQUARE_SMALL)
                if button_a.was_pressed():
                    logg = False
        display.show(Image.YES)
        time.sleep_ms(1000)