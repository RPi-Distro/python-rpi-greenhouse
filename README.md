# Garden Kit

## Components

- Soil Moisture sesnsor - GPIO 14
    
    http://www.instructables.com/id/Soil-Moisture-Sensor-1/?ALLSTEPS

- Temperature and Humidity sensor DHT22 - GPIO 4

    https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/wiring
    
    Uses 10k resistor

- Light sensor - GPIO 18

    https://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi/basic-photocell-reading

- LEDs

    ```
    RED: 16, 11, 23
    WHITE: 13, 9, 27
    GREEN: 21, 12, 25
    BLUE: 20, 6, 22
    ```

- RTC

    http://thepihut.com/blogs/raspberry-pi-tutorials/17209332-adding-a-real-time-clock-to-your-raspberry-pi

## Requirements

- DHT22 requires Adafruit DHT Python library which is not in PyPi and currently Python 2 only:

```bash
sudo apt-get install build-essential python-dev
git clone https://github.com/adafruit/Adafruit_Python_DHT
cd Adafruit_Python_DHT
sudo python setup.py install
cd ..
sudo rm -rf Adafruit_Python_DHT
```
