import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class Veleta:

    def __init__(self):
        self.direccion = "None"

    def iniciarLectura(self):
        # Create the I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        ads = ADS.ADS1115(i2c)

        # Create single-ended input on channel 0
        chan = AnalogIn(ads, ADS.P0)

        # Create differential input between channel 0 and 1
        #chan = AnalogIn(ads, ADS.P0, ADS.P1)

        voltaje = chan.voltage

        return voltaje

    def getDireccion(self):
        voltaje = self.iniciarLectura()

        if (voltaje > 0.100 and voltaje < 0.180):
            self.direccion = "O"
        elif (voltaje >= 0.180 and voltaje < 0.350):
            self.direccion = "NO"
        elif (voltaje >= 0.350 and voltaje < 0.550):
            self.direccion = "N"
        elif (voltaje >= 0.550 and voltaje < 0.900):
            self.direccion = "SO"
        elif (voltaje >= 0.900 and voltaje < 1.300):
            self.direccion = "NE"
        elif (voltaje >= 1.300 and voltaje < 1.950):
            self.direccion = "S"
        elif (voltaje >= 1.300 and voltaje < 1.950):
            self.direccion = "S"
        elif (voltaje >= 1.950 and voltaje < 2.400):
            self.direccion = "SE"
        elif (voltaje >= 2.400 and voltaje < 3.000):
            self.direccion = "E"
        else:
            self.direccion = "None"

        print(self.direccion)


objeto_veleta = Veleta()
objeto_veleta.getDireccion()
