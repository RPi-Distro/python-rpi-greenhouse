from rpi_greenhouse import Greenhouse
from time import sleep

greenhouse = Greenhouse()

greenhouse.record_sensor_values()
greenhouse.export_to_csv()
