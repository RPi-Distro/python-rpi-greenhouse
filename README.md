# Garden Kit

## Components

- Soil Moisture sesnsor - **GPIO 26**
    
    http://www.instructables.com/id/Soil-Moisture-Sensor-1/?ALLSTEPS

- Temperature and Humidity sensor DHT22 - **GPIO 19**

    https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/wiring
    
    Uses 10k resistor

- Light sensor - **GPIO 18**

    https://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi/basic-photocell-reading

- LEDs

    ```
    RED: 16, 11, 23
    WHITE: 13, 9, 27
    GREEN: 21, 12, 25
    BLUE: 20, 6, 22
    ```

- RTC (DS1307)

    - Enable `i2c` in `raspi-config`
    - Add `dtoverlay=i2c-rtc,ds1307` to `/boot/config.txt`
    - Check system date is correct, update if necessary
    - Set RTC from system date with `sudo hwclock -w`
    - Read RTC date with `sudo hwclock -r`

## Requirements

- DHT22 requires Adafruit DHT Python library which is not in PyPi and currently Python 2 only:

```bash
sudo apt-get install build-essential python-dev
git clone https://github.com/adafruit/Adafruit_Python_DHT
cd Adafruit_Python_DHT
sudo python setup.py install
cd ..
sudo rm -rf Adafruit_Python_DHT
git clone https://github.com/bennuttall/garden-kit
```
