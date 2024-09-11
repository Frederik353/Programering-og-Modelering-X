from microbit import *
import radio
radio.on()



while True:
    if button_a.was_pressed():
        radio.send('dot')
    if button_b.was_pressed():
        radio.send('dash')
    r = radio.receive()
    if r == 'dot':
        dislay.show(Image('00000:00000:00900:00000:00000'))
        music.play('F5:1')
        display.clear()
        sleep(300)
    elif r == 'dash':
        dislay.show(Image('00000:00000:99999:00000:00000'))
        music.play('F5:3')
        display.clear()
        sleep(300)