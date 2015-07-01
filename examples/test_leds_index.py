from rpi_greenhouse import GreenhouseIndicator
from time import sleep

indicator = GreenhouseIndicator()

while True:
    for index in range(3):
        indicator.turn_leds_on(index=index)
        print("#%i on" % index)
        sleep(0.5)
        indicator.turn_leds_off(index=index)
