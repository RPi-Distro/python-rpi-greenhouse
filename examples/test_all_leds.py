from rpi_greenhouse import GreenhouseIndicator
from time import sleep

indicator = GreenhouseIndicator()

while True:
    print("All on")
    indicator.turn_leds_on()
    sleep(0.5)
    print("All off")
    indicator.turn_leds_off()
    sleep(0.5)
