from greenhouse import Greenhouse
from time import sleep

greenhouse = Greenhouse()

greenhouse.turn_leds_off()

colours = ['white', 'red', 'blue', 'green']

while True:
    for colour in colours:
        print("%s leds on" % colour)
        greenhouse.turn_leds_on(colour)
        sleep(0.5)
        greenhouse.turn_leds_off(colour)
