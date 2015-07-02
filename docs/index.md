# Raspberry Pi Plantpot Greenhouse

Python module for [Raspberry Pi](https://www.raspberrypi.org/) plantpot greenhouse add-on board produced by [Rachel Rayns](https://github.com/RZRZR). The library provides a simple interface to logging data from the board's sensors, controlling the board's LEDs and using them to display information from the sensors.

**Note: this library is subject to change. Versions below v1.0.0 are considered beta and code may break in future revisions. From the upcoming v1.0.0 release, any changes made will be backwards-compatible with all versions down to v1.0.0.**

## The kit

The Greenhouse kit is currently only available to those participating in the [*BuildYourOwn*](http://craftscouncil.org.uk/what-we-do/build-your-own/) exhibition workshops in Liverpool and Norwich in Summer 2015.

The Raspberry Pi Foundation hopes to make kits available to more people after the exhibitions.

See more information at [raspberrypi.org/garden](https://www.raspberrypi.org/garden/)

### Components

#### Sensors

- Temperature and Humidity sensor (DHT22)
- Soil Moisture sesnsor
- Light sensor (LDR)

#### LEDs

- 3x white
- 3x red
- 3x blue
- 3x green
    
#### RTC

- Real Time Clock (DS1307)

## Installation

Install the dependencies and install `rpi-greenhouse` with `pip`.

See full [installation instructions](installing/).

Python 3 is not currently supported due to a Python 2 -only dependency. This will be resolved as a priority to add Python 3 support.

## Basic Usage

[**Greenhouse**](reference/greenhouse/) - used for accessing values from the sensors and recording them to a database:

```python
from rpi_greenhouse import Greenhouse

greenhouse = Greenhouse()

print(greenhouse.temperature)
greenhouse.record_sensor_values()
```

[**GreenhouseIndicator**](reference/greenhouseindicator/) - used for accessing the sensor values recorded in the database and controlling the board's LEDs

```python
from rpi_greenhouse import GreenhouseIndicator
from time import sleep

greenhouse = GreenhouseIndicator()

while True:
    if indicator.soil_status == 'ok':
        print("Soil ok")
        indicator.turn_leds_on('green')
    if indicator.soil_status == 'low':
        print("Needs watering!")
        indicator.turn_leds_on('red')
    sleep(1)
    indicator.turn_leds_off()
    sleep(1)
```

## Contributors

- [Ben Nuttall](https://github.com/bennuttall) (project maintainer)
- [Tom Hartley](https://github.com/tomhartley)
- [Luke Wren](https://github.com/wren6991)

## Open Source

- The code is licensed under the [BSD Licence](http://opensource.org/licenses/BSD-3-Clause)
- The project source code is hosted on [GitHub](https://github.com/bennuttall/rpi-greenhouse)
- Please use [GitHub issues](https://github.com/bennuttall/rpi-greenhouse/issues) to submit bugs and report issues
