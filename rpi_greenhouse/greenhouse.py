from __future__ import print_function, division
from RPi import GPIO
import sqlite3 as sqlite
from greenhouse_database import GreenhouseDatabase
from datetime import datetime
from time import sleep, time
import math
from sys import exit

try:
    import Adafruit_DHT
except ImportError:
    print("Adafruit DHT library missing.")
    exit(0)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

db = GreenhouseDatabase()


class Greenhouse(object):
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT = 19
    SOIL = 26
    LIGHT = 18

    def __init__(self):
        self.darkness_level = 0.01

        self.humidity, self.temperature = self._get_humidity_and_temperature()
        self.soil = self._get_average_soil_moisture(5)
        self.light = self._get_average_light_level(5)

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
        time_taken = self._time_charging_soil_capacitor()
        totally_wet_time = 8E-6
        totally_dry_time = 0.01
        moisture = (
            math.log(time_taken / totally_dry_time) /
            math.log(totally_wet_time / totally_dry_time)
        )
        return max(0, min(1, moisture)) * 100

    def _time_charging_soil_capacitor(self):
        pin = self.SOIL
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        sleep(0.1)
        GPIO.setup(pin, GPIO.IN)
        start_time = time()
        end_time = time()
        max_time = 1
        while GPIO.input(pin) == GPIO.LOW and time() - start_time < max_time:
            end_time = time()
        time_taken = end_time - start_time
        return time_taken

    def _get_light_level(self):
        time_taken = self._time_charging_light_capacitor()
        value = 100 * time_taken / self.darkness_level
        return 100 - value

    def _time_charging_light_capacitor(self):
        pin = self.LIGHT
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        sleep(0.1)
        GPIO.setup(pin, GPIO.IN)
        start_time = time()
        end_time = time()
        while (
                GPIO.input(pin) == GPIO.LOW and
                time() - start_time < self.darkness_level
            ):
            end_time = time()
        time_taken = end_time - start_time
        return min(time_taken, self.darkness_level)

    def _get_average_soil_moisture(self, num):
        values = [self._get_soil_moisture() for n in range(num)]
        average_value = sum(values) / len(values)
        return average_value

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

    def record_sensor_values(self):
        """
        Save sensor readings to database
        """
        timestamp = self._get_timestamp()
        temperature = self.temperature
        humidity = self.humidity
        soil = self.soil
        light = self.light

        values = (timestamp, temperature, humidity, soil, light)

        db.record_sensor_values(values)

    def export_to_csv(self, file_path=None):
        """
        Export sensor data from database and save as CSV file in file_path
        Defaults to /home/pi/greenhouse.csv
        """
        db.export_to_csv(file_path)

def main():
    greenhouse = Greenhouse()
    greenhouse.record_sensor_values()
    greenhouse.export_to_csv()
    print("Temperature:")
    print(greenhouse.temperature)
    print("Humidity:")
    print(greenhouse.humidity)
    print("Soil:")
    print(greenhouse.soil)
    print("Light:")
    print(greenhouse.light)

if __name__ == '__main__':
    main()
