import Adafruit_BMP.BMP085 as BMP085


class Bmp180:
    '''Lee todos los datos del sensor Bmp180'''

    def __init__(self):
        sensor = BMP085.BMP085()

        self.atm = sensor.read_pressure() / 100
        self.temperatura = sensor.read_temperature()
        self.altura = sensor.read_altitude()

    def get_presion(self):
        '''Devuelve la presión en hPa sin decimales. Es necesario crear un constructor
         Bmp180() para actualizar los datos'''

        return str("{:.0f}".format(self.atm))

    def get_temperatura(self):
        '''Devuelve la temperatura en ºC sin decimales. Es necesario crear un constructor
         Bmp180() para actualizar los datos'''

        return str("{:.0f}".format(self.temperatura))

    def get_altura(self):
        '''Devuelve la altura en metros con un decimal. Es necesario crear un constructor
         Bmp180() para actualizar los datos.

         La altura recibida es muy inexacta.'''

        return str("{:.1f}".format(self.altura))
