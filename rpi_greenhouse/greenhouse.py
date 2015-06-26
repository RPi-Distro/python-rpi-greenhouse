from __future__ import print_function, division
from RPi import GPIO
import sqlite3 as sqlite
from greenhouse_database import GreenhouseDatabase
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

db = GreenhouseDatabase()

class Greenhouse(object):
    LED_COLOURS = [
        'white',
        'red',
        'blue',
        'green',
    ]

    LEDS = {
        'white': [13, 9, 27],
        'red': [16, 11, 23],
        'blue': [20, 6, 22],
        'green': [21, 12, 25],
    }

    SENSOR_LOW = 'low'
    SENSOR_OK = 'ok'
    SENSOR_HIGH = 'high'

    def __init__(self):
        self.target_temperature_lower = 20
        self.target_temperature_upper = 30

        self.target_humidity_lower = 60
        self.target_humidity_upper = 85

        self.target_soil = 60

        self.target_light = 60

        self.status_colours = {
            self.SENSOR_LOW: 'blue',
            self.SENSOR_OK: 'green',
            self.SENSOR_HIGH: 'red',
        }

        self._setup_gpio()

    @property
    def temperature(self):
        return db.get_sensor_value('temperature')

    @property
    def humidity(self):
        return db.get_sensor_value('humidity')

    @property
    def soil(self):
        return db.get_sensor_value('soil')

    @property
    def light(self):
        return db.get_sensor_value('light')

    @property
    def temperature_status(self):
        lower = self.target_temperature_lower
        upper = self.target_temperature_upper

        if lower <= self.temperature <= upper:
            return self.SENSOR_OK
        elif self.temperature < lower:
            return self.SENSOR_LOW
        elif self.temperature > higher:
            return self.SENSOR_HIGH

    @property
    def humidity_status(self):
        lower = self.target_humidity_lower
        upper = self.target_humidity_upper

        if lower <= self.humidity <= upper:
            return self.SENSOR_OK
        elif self.humidity < lower:
            return self.SENSOR_LOW
        elif self.humidity > upper:
            return self.SENSOR_HIGH

    @property
    def soil_status(self):
        if self.soil > self.target_soil:
            return self.SENSOR_OK
        else:
            return self.SENSOR_LOW

    @property
    def light_status(self):
        if self.light >= self.target_light:
            return self.SENSOR_OK
        else:
            return self.SENSOR_LOW

    def _setup_gpio(self):
        for colour in self.LEDS:
            for led in self.LEDS[colour]:
                GPIO.setup(led, GPIO.OUT)
                GPIO.output(led, False)

    def _turn_led_on_or_off(self, colour, index, on_or_off):
        led = self.LEDS[colour][index]
        GPIO.output(led, on_or_off)

    def _turn_led_on(self, colour, index):
        self._turn_led_on_or_off(colour, index, on_or_off=True)

    def _turn_led_off(self, colour, index):
        self._turn_led_on_or_off(colour, index, on_or_off=False)

    def _turn_colour_leds_on_or_off(self, colour, on_or_off):
        leds = self.LEDS[colour]
        for led in range(len(leds)):
            if on_or_off:
                self._turn_led_on(colour, led)
            else:
                self._turn_led_off(colour, led)

    def _turn_colour_leds_on(self, colour):
        self._turn_colour_leds_on_or_off(colour=colour, on_or_off=True)

    def _turn_colour_leds_off(self, colour):
        self._turn_colour_leds_on_or_off(colour=colour, on_or_off=False)

    def _turn_index_leds_on_or_off(self, index, on_or_off):
        for colour in self.LEDS:
            if on_or_off:
                self._turn_led_on(colour, index)
            else:
                self._turn_led_off(colour, index)

    def _turn_index_leds_on(self, index):
        self._turn_index_leds_on_or_off(index=index, on_or_off=True)

    def _turn_index_leds_off(self, index):
        self._turn_index_leds_on_or_off(index=index, on_or_off=False)

    def _turn_all_leds_on_or_off(self, on_or_off):
        for colour in self.LEDS:
            if on_or_off:
                self._turn_colour_leds_on(colour)
            else:
                self._turn_colour_leds_off(colour)

    def _turn_all_leds_on(self):
        self._turn_all_leds_on_or_off(on_or_off=True)

    def _turn_all_leds_off(self):
        self._turn_all_leds_on_or_off(on_or_off=False)

    def turn_leds_on(self, colour=None, index=None):
        """
        Turn LEDs on
        - if colour given, only that colour
        - if index given, only that index
        - if both given, only that LED
        - if neither given, all LEDs

        e.g. turn_leds_on()
        e.g. turn_leds_on(colour='red')
        e.g. turn_leds_on(index=0)
        e.g. turn_leds_on(colour='red', index=0)
        """
        if colour and index is not None:
            self._turn_led_on(colour, index)
        elif colour:
            self._turn_colour_leds_on(colour)
        elif index is not None:
            self._turn_index_leds_on(index)
        else:
            self._turn_all_leds_on()

    def turn_leds_off(self, colour=None, index=None):
        """
        Turn LEDs off
        - if colour given, only that colour
        - if index given, only that index
        - if both given, only that LED
        - if neither given, all LEDs

        e.g. turn_leds_off()
        e.g. turn_leds_off(colour='red')
        e.g. turn_leds_off(index=0)
        e.g. turn_leds_off(colour='red', index=0)
        """
        if colour and index is not None:
            self._turn_led_off(colour, index)
        elif colour:
            self._turn_colour_leds_off(colour)
        elif index is not None:
            self._turn_index_leds_off(index)
        else:
            self._turn_all_leds_off()

    def show_status_on_leds(self):
        """
        Use LEDs to indicate sensor statuses according to self.status_colours
        """
        sensor_statuses = [
            self.temperature_status,
            self.humidity_status,
            self.soil_status,
            self.light_status,
        ]

        for status in sensor_statuses:
            colour = self.status_colours[status]
            self.turn_leds_on(colour)
            sleep(2)
            self.turn_leds_off(colour)
            sleep(0.1)


def main():
    greenhouse = Greenhouse()
    print("Temperature:")
    print(greenhouse.temperature)
    print("Humidity:")
    print(greenhouse.humidity)
    print("Soil:")
    print(greenhouse.soil)
    print("Light:")
    print(greenhouse.light)

    if greenhouse.temperature_status == 'ok':
        print("Temperature ok")
    elif greenhouse.temperature_status == 'low':
        print("Temperature too low")
    elif greenhouse.temperature_status == 'high':
        print("Temperature too high")

    if greenhouse.humidity_status == 'ok':
        print("Humidity ok")
    elif greenhouse.humidity_status == 'low':
        print("Humidity too low")
    elif greenhouse.humidity_status == 'high':
        print("Humidity too high")

    if greenhouse.soil_status == 'ok':
        print("Soil ok")
    else:
        print("Soil too dry")

    if greenhouse.light_status == 'ok':
        print("Light ok")
    else:
        print("Light not ok")

    while True:
        greenhouse.show_status_on_leds()
        sleep(5)

if __name__ == '__main__':
    main()
