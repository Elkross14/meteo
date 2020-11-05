import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
PIN = 18


class Dht11:
    '''Lee todos los datos del sensor Dht11'''

    def __init__(self):
        '''Recoge los datos de temperatura y humedad del sensor DHT11'''

        self.__humidity, self.__temperature = Adafruit_DHT.read_retry(
            sensor, PIN)

    def get_temperature(self):
        '''Devuleve el valor de la temperatura en ºC sin decimales. Es necesario crear un
        constructor Dht11() para actualizar los datos'''

        try:
            return str("{:.0f}".format(self.__temperature))

        # Recogerá el error de lectura del sensor en caso de que no funcione
        except TypeError:
            return str("{:.0f}".format(0))

    def get_humidity(self):
        '''Devuleve el valor de la humedad en % sin decimales. Es necesario crear un constructor
        para actualizar los datos'''

        try:
            return str("{:.0f}".format(self.__humidity))

        except TypeError:
            return str("{:.0f}".format(0))
