# garden-mobile-rasp-hub
## Set-up guide for temperature-humidity sensor
- Set up the bme280 sensor (lecture 6, last slide)
- Enable I2C interface in Raspbery Pi Configuration using `sudo raspi-config`. Then choose Interface Options > I2C
- Install adafruit-circuitpython-bme280 using `sudo python3 -m pip install adafruit-circuitpython-bme280`
- Install sqlite3 using `sudo apt install sqlite3`
- Run the python program
