# GreenhouseIndicator

The `GreenhouseIndicator` class provides access to the most recently recorded sensor values from the database, and the ability to control the board's LEDs.

The sensor values can be read independently, and the LEDs can also be controlled independently of the sensor values, or in conjunction with them (to indicate the status accordingly).

The `GreenhouseIndicator` class should be imported from the module:

```python
from rpi_greenhouse import GreenhouseIndicator
```

Then an instance of a `GreenhouseIndicator` object should be created, e.g:

```python
indicator = GreenhouseIndicator()
```

The initialisation takes optional argument `db_path` which defaults to `/home/pi/.greenhouse/greenhouse.db` - the location the SQLite database file is stored. Users with another username or otherwise wishing to save the database elsewhere should specify the full path here.

e.g:

```python
indicator = GreenhouseIndicator('/root/greenhouse/greenhouse.db')
```

## Properties

### indicator.temperature

Get the last recorded temperature value from the database in degrees Celsius.

### indicator.humidity

Get the last recorded humidity value from the database in percentage (higher value means more humid).

### indicator.soil

Get the last recorded soil moisture value from the database in percentage (0% is totally dry, 100% is totally wet).

### indicator.light

Get the last recorded light level value from the database in percentage (0% is total darkness, 100% is bright light).

### indicator.temperature_status

Get the status of the last recorded temperature value from the database relative to the object's `target_temperature_lower` and `target_temperature_upper` properties.

Possible return values: `'low'`, `'ok'` or `'high'`.

### indicator.humidity_status

Get the status of the last recorded humidity value from the database relative to the object's `target_humidity_lower` and `target_humidity_upper` properties.

Possible return values: `'low'`, `'ok'` or `'high'`.

### indicator.soil_status

Get the status of the last recorded soil moisture value from the database relative to the object's `target_soil` property.

Possible return values: `'low'` or `'ok'`.

### indicator.light_status

Get the status of the last recorded light level value from the database relative to the object's `target_light` property.

Possible return values: `'low'` or `'ok'`.

### indicator.status_colours

Dictionary mapping sensor status values `'low'`, `'ok'` and `'high'` to LED colours. Used in `show_status_on_leds` method.

## Constants

### indicator.LED_COLOURS

List of LED colours in the order in which they appear on the board.

### indicator.SENSOR_*

Optionally use these constants in favour of the simple string equivalents.

- `indicator.SENSOR_LOW` - 'low'
- `indicator.SENSOR_OK` - 'ok'
- `indicator.SENSOR_HIGH` - 'high'

## Methods

### indicator.turn_leds_on()

Turn LEDs on

- if colour given, only that colour
- if index given, only that index
- if both given, only that LED
- if neither given, all LEDs

e.g:

```python
indicator.turn_leds_on()
indicator.turn_leds_on('red')
indicator.turn_leds_on(colour='red')
indicator.turn_leds_on(index=0)
indicator.turn_leds_on('red', 0)
indicator.turn_leds_on(colour='red', index=0)
```

### indicator.turn_leds_off()

Turn LEDs off

- if colour given, only that colour
- if index given, only that index
- if both given, only that LED
- if neither given, all LEDs

e.g:

```python
indicator.turn_leds_off()
indicator.turn_leds_off('red')
indicator.turn_leds_off(colour='red')
indicator.turn_leds_off(index=0)
indicator.turn_leds_off('red', 0)
indicator.turn_leds_off(colour='red', index=0)
```

### indicator.show_status_on_leds()

Use LEDs to indicate sensor statuses according to the object's `status_colours` property. Set to flash once per sensor (temperature, humidity, soil, light) in the colour relating to the status of each sensor. Intended to be looped, e.g:

```python
while True:
    indicator.show_status_on_leds()
    sleep(5)
```
