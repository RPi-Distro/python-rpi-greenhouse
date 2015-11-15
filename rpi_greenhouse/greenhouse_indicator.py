from __future__ import print_function, division
from gpiozero import LEDBoard
from greenhouse_database import GreenhouseDatabase
from time import sleep


class GreenhouseIndicator(object):
    def __init__(self, db_path='/home/pi/.greenhouse/greenhouse.db'):
        """
        db_path defaults to /home/pi/.greenhouse/greenhouse.db
        """
        self.db = GreenhouseDatabase(db_path)

        self.white = LEDBoard(13, 9, 27)
        self.red = LEDBoard(16, 11, 23)
        self.blue = LEDBoard(20, 6, 22)
        self.green = LEDBoard(21, 12, 25)

        self.target_temperature_lower = 20
        self.target_temperature_upper = 30

        self.target_humidity_lower = 60
        self.target_humidity_upper = 85

        self.target_soil = 60

        self.target_light = 60

        self.SENSOR_LOW = 'low'
        self.SENSOR_OK = 'ok'
        self.SENSOR_HIGH = 'high'

        self.status_colours = {
            self.SENSOR_LOW: 'blue',
            self.SENSOR_OK: 'green',
            self.SENSOR_HIGH: 'red',
        }

        self._colour_ledboards = {
            'white': self.white,
            'red': self.red,
            'blue': self.blue,
            'green': self.green,
        }

    def on(self):
        for leds in self._colour_ledboards.values():
            leds.on()

    def off(self):
        for leds in self._colour_ledboards.values():
            leds.off()

    @property
    def temperature(self):
        return self.db.get_sensor_value('temperature')

    @property
    def humidity(self):
        return self.db.get_sensor_value('humidity')

    @property
    def soil(self):
        return self.db.get_sensor_value('soil')

    @property
    def light(self):
        return self.db.get_sensor_value('light')

    @property
    def temperature_status(self):
        lower = self.target_temperature_lower
        upper = self.target_temperature_upper

        if lower <= self.temperature <= upper:
            return self.SENSOR_OK
        elif self.temperature < lower:
            return self.SENSOR_LOW
        elif self.temperature > upper:
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

    def show_status_on_leds(self, on_time=2, off_time=0.1):
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
            leds = self._colour_ledboards[colour]
            leds.on()
            sleep(on_time)
            leds.off()
            sleep(off_time)
