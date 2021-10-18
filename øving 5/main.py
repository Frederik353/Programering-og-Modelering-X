from microbit import *
import time



while True:
    logg = True 
    display.scroll ("Press A to start logging", delay = 75)
    if button_a.was_pressed():
        with open("temperature.txt", "w") as f:
            while logg:
                currentTemp = temperature()
                f.write(str(currentTemp) + "\n")
                print((currentTemp,))
                display.clear()
                # start = time.ticks_ms()
                # while(time.ticks_diff(time.ticks_ms(), start) < 1000 ):
                time.sleep_ms(1000)
                if button_a.was_pressed():
                    logg = False
                display.show(Image.SQUARE_SMALL)
        display.show(Image.YES)
        time.sleep_ms(1000)