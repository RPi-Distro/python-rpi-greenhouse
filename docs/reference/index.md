# API Reference

The `rpi-greenhouse` module exposes two classes - `Greenhouse` and `GreenhouseIndicator`.

Use `Greenhouse` to access real-time sensor data, and use `GreenhouseIndicator` to access the latest sensor values saved in the database, and to control the board's LEDs.

These classes are intended for use simultaneously, and do not interfere with each other.

## Classes

### Greenhouse

The `Greenhouse` class provides direct access to the sensors (temperature, humidity, soil moisture and light), and the ability to log sensor values to a database and export the database to CSV.

See [Greenhouse](/reference/greenhouse/).

### GreenhouseIndicator

The `GreenhouseIndicator` class provides access to the most recently recorded sensor values from the database, and the ability to control the board's LEDs.

The sensor values can be read independently, and the LEDs can also be controlled independently of the sensor values, or in conjunction with them (to indicate the status accordingly).

See [GreenhouseIndicator](/reference/greenhouseindicator/).

## Version

```python
import rpi_greenhouse
print(rpi_greenhouse.__version__)
```

Provides the version number of the `rpi-greenhouse` package.
