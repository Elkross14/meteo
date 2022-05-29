import Adafruit_BMP.BMP085 as BMP085  # Imports the BMP library

# Create an 'object' containing the BMP180 data
try:
    sensor = BMP085.BMP085()

    # Temperature in Celcius
    print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
    # The local pressure
    print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
    # The current altitude
    print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
    # The sea-level pressure
    print('Sealevel Pressure = {0:0.2f} Pa'.format(
        sensor.read_sealevel_pressure()))

except OSError:
    print("error")
