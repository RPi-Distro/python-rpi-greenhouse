from __future__ import print_function, division
from RPi import GPIO
import Adafruit_DHT
import sqlite3 as sqlite
from datetime import datetime
from time import sleep, time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

db = sqlite.connect("/home/pi/db/greenhouse.db")
cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS
        greenhouse (
            datetime TEXT,
            temperature REAL,
            humidity REAL,
            soil REAL,
            light REAL
        )
""")
db.commit()


class Greenhouse(object):
    LEDS = {
        'white': [13, 9, 27],
        'red': [16, 11, 23],
        'blue': [20, 6, 22],
        'green': [21, 12, 25],
    }

    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT = 19
    SOIL = 26
    LIGHT = 18

    SENSOR_LOW = 'low'
    SENSOR_OK = 'ok'
    SENSOR_HIGH = 'high'

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
        if self.soil:
            return self.SENSOR_OK
        else:
            return self.SENSOR_LOW

    @property
    def light_status(self):
        if self.light >= self.target_light:
            return self.SENSOR_OK
        else:
            return self.SENSOR_LOW

    def __init__(self, use_sensors=True):
        self.use_sensors = use_sensors

        self.target_temperature_lower = 20
        self.target_temperature_upper = 30

        self.target_humidity_lower = 40
        self.target_humidity_upper = 60

        self.target_light = 60

        self.status_colours = {
            self.SENSOR_LOW: 'blue',
            self.SENSOR_OK: 'green',
            self.SENSOR_HIGH: 'red',
        }

        self._setup_gpio()

        if use_sensors:
            self.update_sensor_values()
        else:
            self._get_sensor_values_from_database()

    def _setup_gpio(self):
        for colour in self.LEDS:
            for led in self.LEDS[colour]:
                GPIO.setup(led, GPIO.OUT)
                GPIO.output(led, False)

    def _get_sensor_values_from_database(self):
        cursor.execute("""
            SELECT
                *
            FROM
                greenhouse
            ORDER BY
                datetime(datetime) DESC
            LIMIT
                0, 1
        """)
        result = cursor.fetchone()
        datetime, temperature, humidity, soil, light = result

        self.temperature = temperature
        self.humidity = humidity
        self.soil = soil
        self.light = light

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

    def _get_humidity_and_temperature(self):
        humidity, temperature = Adafruit_DHT.read_retry(
            sensor=self.DHT_SENSOR,
            pin=self.DHT,
            retries=5
        )
        self.humidity = humidity
        self.temperature = temperature
        return (humidity, temperature)

    def _get_soil_moisture(self):
        pin = self.SOIL
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        sleep(0.1)
        GPIO.setup(pin, GPIO.IN)

        start_time = time()
        end_time = time()
        max_time = 1
        while GPIO.input(pin) == GPIO.LOW:
            end_time = time()
            if (end_time - start_time) > max_time:
                end_time = start_time + max_time
                break

        time_taken = end_time - start_time
        value = 1 - (time_taken / max_time)
        return value

    def _get_light_level(self):
        pin = self.LIGHT
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        sleep(0.1)
        GPIO.setup(pin, GPIO.IN)
        start_time = time()
        while GPIO.input(pin) == GPIO.LOW:
            end_time = time()
            if ((end_time - start_time) * 10000) > 100:
                return 0
        end_time = time()
        return 100 - ((end_time - start_time) * 10000)

    def _get_average_soil_moisture(self, num):
        values = [self._get_soil_moisture() for n in range(num)]
        average_value = sum(values) / len(values)
        return round(average_value) == 1

    def _get_average_light_level(self, num):
        values = [self._get_light_level() for n in range(num)]
        average_value = sum(values) / len(values)
        return average_value

    def _get_timestamp(self):
        dt = datetime.now()
        dt_date = str(dt.date())
        dt_time = str(dt.time())
        timestamp = "%s %s" % (dt_date, dt_time[:8])
        return timestamp

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
        if colour and index:
            self._turn_led_off(colour, index)
        elif colour:
            self._turn_colour_leds_off(colour)
        elif index:
            self._turn_index_leds_off(index)
        else:
            self._turn_all_leds_off()

    def update_sensor_values(self):
        self._get_humidity_and_temperature()
        self.get_soil()
        self.get_light()

    def get_temperature(self):
        """
        Return temperature value from sensor, in degrees Celsius

        (use self.temperature for cached value)
        """
        if not self.use_sensors:
            raise Exception('Initialised without sensors.')

        humidity, temperature = self._get_humidity_and_temperature()
        self.temperature = temperature
        return temperature

    def get_humidity(self):
        """
        Return humidity value from sensor, in percentage

        (use self.humidity for cached value)
        """
        if not self.use_sensors:
            raise Exception('Initialised without sensors.')

        humidity, temperature = self._get_humidity_and_temperature()
        self.humidity = humidity
        return humidity

    def get_soil(self):
        """
        Return soil moisture value from sensor - True (wet) or False (dry)

        (use self.soil for cached value)
        """
        if not self.use_sensors:
            raise Exception('Initialised without sensors.')

        soil = self._get_average_soil_moisture(5)
        self.soil = soil
        return self.soil

    def get_light(self):
        """
        Return light value from sensor, in percentage

        (use self.light for cached value)
        """
        if not self.use_sensors:
            raise Exception('Initialised without sensors.')

        self.light = self._get_average_light_level(5)
        return self.light

    def record_sensor_values(self):
        """
        Save sensor readings to database
        """
        if not self.use_sensors:
            raise Exception('Initialised without sensors.')

        timestamp = self._get_timestamp()
        temperature = self.temperature
        humidity = self.humidity
        soil = "%i" % self.soil
        light = self.light

        values = (timestamp, temperature, humidity, soil, light)
        cursor.execute("""
            INSERT INTO
                greenhouse
            VALUES
                (?, ?, ?, ?, ?)
        """, values)
        db.commit()

    def export_to_csv(self, file_path):
        """
        Export sensor data from database and save as CSV file in file_path
        """
        cursor.execute("""
            SELECT
                *
            FROM
                greenhouse
        """)
        results = cursor.fetchall()
        with open(file_path, 'w') as f:
            for result in results:
                for data in result:
                    f.write('%s,' % data)
                f.write('\n')

    def show_status_on_leds(self):
        """
        Use LEDs to indicate sensor statuses according to self.status_colours
        """
        if not self.use_sensors:
            self._get_sensor_values_from_database()

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
    greenhouse.record_sensor_values()
    greenhouse.export_to_csv('/home/pi/test.csv')
    print("Temperature: %f" % greenhouse.temperature)
    print("Humidity: %f" % greenhouse.humidity)
    print("Soil: %f" % greenhouse.soil)
    print("Light: %f" % greenhouse.light)

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
