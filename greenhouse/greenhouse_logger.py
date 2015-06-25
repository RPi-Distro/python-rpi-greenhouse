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


class GreenhouseLogger(object):
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT = 19
    SOIL = 26
    LIGHT = 18

    def __init__(self):
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
        cursor.execute("""
            INSERT INTO
                greenhouse
            VALUES
                (?, ?, ?, ?, ?)
        """, values)
        db.commit()


def main():
    logger = GreenhouseLogger()
    logger.record_sensor_values()
    print("Temperature: %f" % logger.temperature)
    print("Humidity: %f" % logger.humidity)
    print("Soil: %f" % logger.soil)
    print("Light: %f" % logger.light)

if __name__ == '__main__':
    main()
