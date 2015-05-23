import Adafruit_DHT

SENSOR = Adafruit_DHT.DHT22
PIN = 4

def get_temperature_and_humidity(pin=PIN):
    return Adafruit_DHT.read_retry(SENSOR, pin)

def get_temperature(pin=PIN):
    temperature_and_humidity = get_temperature_and_humidity(pin)
    return temperature

def get_humidity(pin=PIN):
    temperature_and_humidity = get_temperature_and_humidity(pin)
    return humidity

def main():
    pin = 4
    temperature, humidity = get_temperature_and_humidity(pin)
    print('Temperature: {0:0.1f}*C  Humidity: {1:0.1f}%'.format(temperature, humidity))

if __name__ == '__main__':
    main()
