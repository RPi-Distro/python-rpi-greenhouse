from rpi_greenhouse import GreenhouseIndicator
from time import sleep

indicator = GreenhouseIndicator()

colours = ['white', 'red', 'blue', 'green']

while True:
    for index in range(3):
        for colour in colours:
            indicator.turn_leds_on(colour, index)
            print("%s #%i on" % (colour, index))
            sleep(0.1)
            indicator.turn_leds_off(colour, index)
