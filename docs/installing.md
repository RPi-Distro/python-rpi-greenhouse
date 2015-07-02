# Installing, updating and removing

Manage your installation of the `rpi-greenhouse` package with `pip`.

## Python 2:

Install dependencies:

```bash
sudo apt-get install build-essential python-dev python-pip
git clone https://github.com/adafruit/Adafruit_Python_DHT
cd Adafruit_Python_DHT
sudo python setup.py install
cd ..
rm -rf Adafruit_Python_DHT
```

Install `rpi-greenhouse` with `pip`:

```bash
sudo pip install rpi-greenhouse
```

## Python 3

The library does not currently support Python 3 due to the dependency on [Adafruit Python DHT](https://github.com/adafruit/Adafruit_Python_DHT). This will be resolved as a priority to add Python 3 support.

## Version checking

Check which version of `rpi-greenhouse` you have installed by inspecting `__version__`:

```python
import rpi_greenhouse

print(rpi_greenhouse.__version__)
```

or in one line from the command line:

```bash
python -c "import rpi_greenhouse as g; print(g.__version__)"
```

## Updating

Update to the latest version of `rpi-greenhouse` with:

```bash
sudo pip install rpi-greenhouse --upgrade
```

## Removing

Uninstall the package with:

```bash
sudo pip uninstall rpi-greenhouse
```
