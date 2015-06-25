from greenhouse import Greenhouse
from time import sleep

greenhouse = Greenhouse()

while True:
    greenhouse.show_status_on_leds()
    sleep(5)
