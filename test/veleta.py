import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class Veleta:

    def __init__(self):
        self.direccion = "None"

    def iniciarLectura(self):
        '''Hace la lectura del voltaje de salida de la veleta'''

        # Crear el bus I2C
        i2c = busio.I2C(board.SCL, board.SDA)

        # Creando el objeto ADC mediante el bus I2C
        ads = ADS.ADS1115(i2c)

        # Creando una entrada para el canal 0 del ADC
        chan = AnalogIn(ads, ADS.P0)

        # Creando una entrada para los canales 0 y 1
        #chan = AnalogIn(ads, ADS.P0, ADS.P1)

        # Lectura del dato
        voltaje = chan.voltage

        return voltaje

    def getDireccion(self):
        '''Mediante el voltaje de salida de la veleta determinará
        la dirección del viento Devolviendo así un String con el
        resultado'''

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

        return self.direccion


objeto_veleta = Veleta()
print(objeto_veleta.getDireccion())
