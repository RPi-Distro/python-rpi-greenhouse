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


RED_LEDS = [16, 20, 21, 26]
WHITE_LEDS = [6, 12, 13, 19]
GREEN_LEDS = [9, 11, 25, 8]
YELLOW_LEDS = [27, 22, 23, 24]

LEDS = RED_LEDS + WHITE_LEDS + GREEN_LEDS + YELLOW_LEDS

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
