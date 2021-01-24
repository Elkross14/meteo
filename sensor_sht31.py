import board
import busio
import adafruit_sht31d
import logging


class Sht31:
    '''Lee todos los datos del sensor SHT31'''

    def __init__(self, address):

        try:

            i2c = busio.I2C(board.SCL, board.SDA)

            sensor = adafruit_sht31d.SHT31D(i2c, address)

            self.humedad = sensor.relative_humidity
            self.temperatura = sensor.temperature

        # Recoge el error de lectura del canal SDA
        except (ValueError, OSError):
            logging.error('El sensor SHT31 ha dejado de funcionar.')
            self.humedad = -100
            self.temperatura = -100

    def get_humedad(self):
        '''Devuelve la humedad en % sin decimales en String. Es necesario
        crear un constructor Sht31(address) para actualizar los datos'''

        return str(round(self.humedad))

    def get_temperatura(self):
        '''Devuelve la temperatura en ºC sin decimales en String. Es necesario
        crear un constructor Sht31(address) para actualizar los datos'''

        return str(round(self.temperatura))
