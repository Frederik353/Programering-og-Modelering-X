from microbit import *
import music
import radio
radio.config(group=9)
radio.on()

MORSE = {
    ".-": "A",
    "-...": "B",
    "-.-.": "C",
    "-..": "D",
    ".": "E",
    "..-.": "F",
    "--.": "G",
    "....": "H",
    "..": "I",
    ".---": "J",
    "-.-": "K",
    ".-..": "L",
    "--": "M",
    "-.": "N",
    "---": "O",
    ".--.": "P",
    "--.-": "Q",
    ".-.": "R",
    "...": "S",
    "-": "T",
    "..-": "U",
    "...-": "V",
    ".--": "W",
    "-..-": "X",
    "-.--": "Y",
    "--..": "Z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    "-----": "0"
}

dot_img = Image('00000:00000:00900:00000:00000:')
DOTLEN = 230
DASHLEN = 470

LETTER_THRESHOLD = 1000

buffer = ''
message = ''
started_to_wait = running_time()

def decode(buffer):
    return MORSE.get(buffer, '?')

while True:
    waiting = running_time() - started_to_wait
    signal = radio.receive()
    if button_a.is_pressed():
        display.show(dot_img)
        radio.send('.')
        sleep(300) 
        display.clear()
    elif button_b.is_pressed():
        display.show('-')
        radio.send('-')
        sleep(300)
        display.clear()
    if signal:
        if signal == '.':
            buffer += '.'
            display.show('.')
            sleep(DOTLEN)
            display.clear()
        elif signal == '-':
            buffer += '-'
            display.show('-')
            sleep(DASHLEN)
            display.clear()
        started_to_wait = running_time()
    elif len(buffer) > 0 and waiting > LETTER_THRESHOLD:
        character = decode(buffer)
        buffer = ''
        display.show(character)
        message += character
    if accelerometer.was_gesture('shake'):
        display.scroll(message)
        message = ''