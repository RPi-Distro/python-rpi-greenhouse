from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def setup_leds():
    for led in LEDS:
        GPIO.setup(led, GPIO.OUT, False)

def control_leds(leds=None, on_or_off=True, pause=0, backwards=False):
    if leds is None:
        leds = LEDS

    if backwards:
        leds = reversed(leds)

    for led in leds:
        GPIO.output(led, on_or_off)
        sleep(pause)

RED_LEDS = [16, 11, 23]
WHITE_LEDS = [13, 9, 27]
GREEN_LEDS = [21, 12, 25]
BLUE_LEDS = [20, 6, 22]

LEDS = RED_LEDS + WHITE_LEDS + GREEN_LEDS + BLUE_LEDS

setup_leds()

def main():
    print("Turning LEDs on")
    control_leds(on_or_off=True, pause=0.1)
    print("All LEDs should now be on")
    sleep(5)
    print("Turning LEDs off")
    control_leds(on_or_off=False, pause=0.1, backwards=True)
    print("All LEDs should now be off")


if __name__ == '__main__':
    main()
