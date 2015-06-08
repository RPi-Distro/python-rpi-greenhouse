from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIN = 18

def get_light_sensor_value(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    sleep(0.1)
    GPIO.setup(pin, GPIO.IN)
    reading = 0
    while GPIO.input(pin) == GPIO.LOW:
            reading += 1
    return reading

def main():
    while True:
        print(get_light_sensor_value(PIN))


if __name__ == '__main__':
    main()
