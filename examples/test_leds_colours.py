from rpi_greenhouse import GreenhouseIndicator
from time import sleep

indicator = GreenhouseIndicator()

colours = indicator.LED_COLOURS

while True:
    for colour in colours:
        print("%s leds on" % colour)
        indicator.turn_leds_on(colour)
        sleep(0.5)
        indicator.turn_leds_off(colour)
