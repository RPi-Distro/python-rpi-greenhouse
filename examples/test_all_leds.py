from greenhouse import Greenhouse
from time import sleep

greenhouse = Greenhouse()

while True:
    print("All on")
    greenhouse.turn_leds_on()
    sleep(0.5)
    print("All off")
    greenhouse.turn_leds_off()
    sleep(0.5)
