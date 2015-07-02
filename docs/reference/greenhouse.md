# Greenhouse

The `Greenhouse` class provides direct access to the sensors (temperature, humidity, soil moisture and light), and the ability to log sensor values to a database and export the database to CSV.

The `Greenhouse` class should be imported from the module:

```python
from rpi_greenhouse import Greenhouse
```

Then an instance of a `Greenhouse` object should be created, e.g:

```python
greenhouse = Greenhouse()
```

The initialisation takes optional argument `db_path` which defaults to `/home/pi/.greenhouse/greenhouse.db` - the location the SQLite database file is stored. Users with another username or otherwise wishing to save the database elsewhere should specify the full path here.

e.g:

```python
indicator = Greenhouse('/root/greenhouse/greenhouse.db')
```

## Properties

### greenhouse.temperature

Calculated property - get the temperature value from the temperature sensor in degrees Celsius.

### greenhouse.humidity

Calculated property - get the humidity value from the humidity sensor in percentage (higher value means more humid).

### greenhouse.soil

Calculated property - get the soil moisture value from the soil moisture sensor in percentage (0% is totally dry, 100% is totally wet).

### greenhouse.light

Calculated property - get the light level value from the light sensor in percentage (0% is total darkness, 100% is bright light).

Note: Use `greenhouse.darkness_level` to calibrate your light sensor.

### greenhouse.darkness_level

Default: `0.01`

Set the darkness level to improve the accuracy of your light sensor.

## Methods

The following methods are available:

### greenhouse.record_sensor_values()

Take all sensor readings and record to the database.

Arguments: None

### greenhouse.export_to_csv()

Export sensor data from database and save as CSV file.

Arguments:

- `file_path` (default: `'/home/pi/greenhouse.csv'`)
