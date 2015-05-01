from RPi import GPIO
from time import time, sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def get_soil_moisture(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    sleep(0.1)
    GPIO.setup(pin, GPIO.IN)
    start_time = time()
    while GPIO.input(pin) == GPIO.LOW:
        pass
    end_time = time()
    return end_time - start_time

def main():
    soil = 14

    while True:
        print(get_soil_moisture(soil))


if __name__ == '__main__':
    main()
