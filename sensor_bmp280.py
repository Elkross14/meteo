import board
import adafruit_bmp280


class Bmp280:  # Creamos una clase específica para el sensor
    '''Lee todos los datos del sensor Bmp280'''

    def __init__(self):

        try:
            i2c = board.I2C()
            # Creamos el constructor que lee los datos
            sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

            # Se le suma 8 a la presión porque tras meses de pruebas se observa que
            # el sensor venia mal calibrado.
            self.atm = sensor.pressure
            self.temperatura = sensor.temperature

        # Recoge el error de lectura del canal SDA
        except OSError:
            logging.error('El sensor BMP280 ha dejado de funcionar.')
            self.atm = -100
            self.temperatura = -100

    def get_presion(self):
        '''Devuelve la presión en hPa sin decimales en String. Es necesario crear
        un constructor Bmp280() para actualizar los datos'''

        return str(round(self.atm))

    def get_temperatura(self):
        '''Devuelve la temperatura en ºC sin decimales en String. Es necesario crear
        un constructor Bmp280() para actualizar los datos'''

        return str(round(self.temperatura))
