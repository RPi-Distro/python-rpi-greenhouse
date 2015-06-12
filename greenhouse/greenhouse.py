from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Greenhouse(object):
    leds = {
        'red': [16, 11, 23],
        'white': [13, 9, 27],
        'green': [21, 12, 25],
        'blue': [20, 6, 22],
    }

    def __init__(self):
        self._setup_gpio()

    def _setup_gpio(self):
        for colour in self.leds:
            for led in self.leds[colour]:
                GPIO.setup(led, GPIO.OUT)
                GPIO.output(led, False)

    def _turn_led_on_or_off(self, colour, index, on_or_off):
        led = self.leds[colour][index]
        GPIO.output(led, on_or_off)

    def _turn_colour_leds_on_or_off(self, colour, on_or_off):
        leds = self.leds[colour]
        for led in range(len(leds)):
            if on_or_off:
                self.turn_led_on(colour, led)
            else:
                self.turn_led_off(colour, led)

    def _turn_all_leds_on_or_off(self, on_or_off):
        for colour in self.leds:
            if on_or_off:
                self.turn_colour_leds_on(colour)
            else:
                self.turn_colour_leds_off(colour)

    def turn_led_on(self, colour, index):
        """
        Turn a single LED on, by colour and index

        e.g. turn_led_on('red', 0)
        """
        self._turn_led_on_or_off(colour, index, on_or_off=True)

    def turn_led_off(self, colour, index):
        """
        Turn a single LED off, by colour and index

        e.g. turn_led_off('red', 0)
        """
        self._turn_led_on_or_off(colour, index, on_or_off=False)

    def turn_colour_leds_on(self, colour):
        """
        Turn all LEDs of a particular colour on

        e.g. turn_colour_leds_on('red')
        """
        self._turn_colour_leds_on_or_off(colour, on_or_off=True)

    def turn_colour_leds_off(self, colour):
        """
        Turn all LEDs of a particular colour off

        e.g. turn_colour_leds_off('red')
        """
        self._turn_colour_leds_on_or_off(colour, on_or_off=False)

    def turn_all_leds_on(self):
        """
        Turn all LEDs on
        """
        self._turn_all_leds_on_or_off(on_or_off=True)

    def turn_all_leds_off(self):
        """
        Turn all LEDs off
        """
        self._turn_all_leds_on_or_off(on_or_off=False)

def main():
    greenhouse = Greenhouse()
    greenhouse.turn_all_leds_on()
    sleep(2)
    greenhouse.turn_all_leds_off()
    sleep(2)
    for colour in greenhouse.leds:
        greenhouse.turn_colour_leds_on(colour)
        sleep(2)
        greenhouse.turn_colour_leds_off(colour)

if __name__ == '__main__':
    main()
