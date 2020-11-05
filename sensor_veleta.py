import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class Veleta:
    '''Le la dirección del viento mediante la veleta.'''

    def __init__(self):
        self.direccion = "None"

    def iniciar_lectura(self):
        '''Crea un objeto del chip ADS1115 para poder leer los datos de la veleta.'''

        # Crea un bus I2C
        i2c = busio.I2C(board.SCL, board.SDA)

        try:
            # Crea un objeto ADC usando el bus I2C
            ads = ADS.ADS1115(i2c)

            # Entrada del canal 0 del chip
            chan = AnalogIn(ads, ADS.P0)

            voltaje = chan.voltage

        # Recoge el error de lectura del canal SDA
        except ValueError:
            voltaje = 0

        return voltaje

    def get_direccion_viento(self):
        '''Lee el voltaje de la veleta y lo pasa a la dirección adecuada. Hay 8 direcciones
        posibles'''

        voltaje = self.iniciar_lectura()

        if 100 < voltaje < 0.180:
            self.direccion = "O"
        elif 0.180 < voltaje < 0.350:
            self.direccion = "NO"
        elif 0.350 < voltaje < 0.550:
            self.direccion = "N"
        elif 0.550 < voltaje < 0.900:
            self.direccion = "SO"
        elif 0.900 < voltaje < 1.300:
            self.direccion = "NE"
        elif 1.300 < voltaje < 1.950:
            self.direccion = "S"
        elif 1.300 < voltaje < 1.950:
            self.direccion = "S"
        elif 1.950 < voltaje < 2.400:
            self.direccion = "SE"
        elif 2.400 < voltaje < 3.000:
            self.direccion = "E"
        else:
            self.direccion = "None"

        return self.direccion
