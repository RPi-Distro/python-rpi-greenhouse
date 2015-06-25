from greenhouse import Greenhouse
from time import sleep

greenhouse = Greenhouse()

colours = ['white', 'red', 'blue', 'green']

while True:
    for index in range(3):
        for colour in colours:
            greenhouse.turn_leds_on(colour, index)
            print("%s #%i on" % (colour, index))
            sleep(0.1)
            greenhouse.turn_leds_off(colour, index)
