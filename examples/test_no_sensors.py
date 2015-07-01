from rpi_greenhouse import GreenhouseIndicator
from time import sleep

indicator = GreenhouseIndicator()

while True:
    indicator.show_status_on_leds()
    sleep(5)
