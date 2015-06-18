from __future__ import print_function
from RPi import GPIO
from time import time, sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIN = 18

def get_light_level(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    sleep(0.1)
    GPIO.setup(pin, GPIO.IN)
    start_time = time()
    while GPIO.input(pin) == GPIO.LOW:
        pass
    end_time = time()
    return (end_time - start_time) * 10000

def main():
    light_values = []
    for i in range(20):
        light = get_light_level(PIN)
        light_values.append(light)
    print("min: %f" % min(light_values))
    print("max: %f" % max(light_values))
    print("avg: %f" % (sum(light_values) / float(len(light_values))))



if __name__ == '__main__':
    main()
