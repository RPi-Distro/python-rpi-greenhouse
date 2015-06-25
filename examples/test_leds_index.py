from greenhouse import Greenhouse
from time import sleep

greenhouse = Greenhouse()

while True:
    for index in range(3):
        greenhouse.turn_leds_on(index=index)
        print("#%i on" % index)
        sleep(0.5)
        greenhouse.turn_leds_off(index=index)
