import Adafruit_BMP.BMP085 as BMP085

sensor = BMP085.BMP085()

#calculo de Pa a atm
atm = sensor.read_pressure() / 101325
print('Temperatura BMP180 = {0:0.2f} ºC'.format(sensor.read_temperature()))
print('Presión = {0:0.2f} atm'.format(atm))
print('Altitud = {0:0.2f} m'.format(sensor.read_altitude()))
