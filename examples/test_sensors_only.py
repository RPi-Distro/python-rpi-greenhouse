from greenhouse_logger import GreenhouseLogger
from time import sleep

logger = GreenhouseLogger()
while True:
    logger.record_sensor_values()
    print("done")
    sleep(30)
