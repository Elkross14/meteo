import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import logging


class Veleta:
    '''Le la dirección del viento. Se divide en 8 direcciones diferentes'''

    direccion = "None"
    funcionamiento = True

    def __init__(self):

        try:
            # Crear el bus I2C
            i2c = busio.I2C(board.SCL, board.SDA)

            # Creando el objeto ADC mediante el bus I2C
            ads = ADS.ADS1115(i2c)

            # Creando una entrada para el canal 0 del ADC
            chan = AnalogIn(ads, ADS.P0)

            # Lectura del dato
            self.voltaje = chan.voltage

            self.calcular_direccion(self.voltaje)

        except (ValueError, OSError):
            self.funcionamiento = False

            logging.error('El ADC de la veleta ha dejado de funcionar.')

    def calcular_direccion(self, voltaje):
        '''El voltaje determina el angulo de rotación de la veleta.
        Sabiendo el voltaje de salida en cada angulo sabemos la dirección
        del viento'''

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

    def get_direccion(self):
        '''Mediante el voltaje de salida de la veleta determinará
        la dirección del viento Devolviendo así un String con el
        resultado'''

        return self.direccion

    def get_funcionamiento(self):
        '''Nos dice mediante un boolean si el sensor funciona. En el caso de True
        es que el sensor funciona'''

        return self.funcionamiento
