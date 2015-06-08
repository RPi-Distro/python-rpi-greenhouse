import Adafruit_DHT

SENSOR = Adafruit_DHT.DHT22
PIN = 19

def get_humidity_and_temperature(pin):
    """
    Returns a (humidity, temperature) tuple
    """

    return Adafruit_DHT.read_retry(SENSOR, pin)

def get_humidity(pin):
    """
    Returns the humidity value
    """

    humidity, temperature = get_humidity_and_temperature(pin)
    return humidity

def get_temperature(pin):
    """
    Returns the temperature value
    """

    humidity, temperature = get_humidity_and_temperature(pin)
    return temperature

def main():
    humidity, temperature = get_humidity_and_temperature(PIN)
    print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))

if __name__ == '__main__':
    main()
