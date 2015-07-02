import os
from setuptools import setup, find_packages
from rpi_greenhouse import __version__


description = """
    Simple interface to Raspberry Pi Plantpot Greenhouse add-on board
"""


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="rpi-greenhouse",
    version=__version__,
    author="Ben Nuttall",
    author_email="ben@raspberrypi.org",
    description=description.strip(),
    long_description=read('README.rst'),
    license="BSD",
    keywords=[
        "raspberry pi",
        "greenhouse",
        "garden",
        "plant",
        "sensor",
    ],
    url="https://github.com/bennuttall/rpi-greenhouse",
    packages=find_packages(),
    install_requires=[
        "RPi.GPIO",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2",
        "Topic :: Home Automation",
        "Topic :: Education",
        "License :: OSI Approved :: BSD License",
    ],
)
