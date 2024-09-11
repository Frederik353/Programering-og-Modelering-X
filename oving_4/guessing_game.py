from microbit import *
import random
import time





while True:
    num1 = random.randint(1, 9)
    num2 = random.randint(1, 9)
    answer = num1 * num2

    display.scroll(str(num1) + "x" + str(num2))
    guess = 0
    dump = button_a.get_presses() + button_b.get_presses()

    while (not button_a.is_pressed()) and (not button_b.is_pressed()):
        guess += button_a.get_presses() + button_b.get_presses() * 10
        if guess > 9:
            display.scroll(str(guess))
        else:
            display.show(str(guess))
        start = time.ticks_ms()
        while(time.ticks_diff(time.ticks_ms(), start) < 1000 ):
            pass

    if guess == answer:
        display.show(Image.YES)
        display.scroll(str(guess))
        sleep(1000)
    else:
        display.show(Image.NO)
        sleep(1000)
        display.scroll("you guessed " + str(guess) + ", the correctt answer is " + str(answer),delay=75)
