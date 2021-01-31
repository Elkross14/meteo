import Adafruit_BMP.BMP085 as BMP085  # Importamos la libreria BMP
import logging


class Bmp180:  # Creamos una clase específica para el sensor
    '''Lee todos los datos del sensor Bmp180'''

    def __init__(self):

        try:
            sensor = BMP085.BMP085()  # Creamos el constructor que lee los datos

            # Se le suma 8 a la presión porque tras meses de pruebas se observa que
            # el sensor venia mal calibrado.
            self.atm = (sensor.read_pressure() / 100) + 8
            self.temperatura = sensor.read_temperature()
            self.altura = sensor.read_altitude()

        # Recoge el error de lectura del canal SDA
        except OSError:
            logging.error('El sensor BMP180 ha dejado de funcionar.')
            self.atm = -100
            self.temperatura = -100
            self.altura = -100

    def get_presion(self):
        '''Devuelve la presión en hPa sin decimales en String. Es necesario crear
        un constructor Bmp180() para actualizar los datos'''

        return str(round(self.atm))

    def get_temperatura(self):
        '''Devuelve la temperatura en ºC sin decimales en String. Es necesario crear
        un constructor Bmp180() para actualizar los datos'''

        return str(round(self.temperatura))

    def get_altura(self):
        '''Devuelve la altura en metros sin decimales en String. Es necesario
        crear un constructor Bmp180() para actualizar los datos. La altura recibida
        es muy inexacta.'''

        return str(round(self.altura))
