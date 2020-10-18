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
        '''Devuleve el valor de la temperatura en ºC. Es necesario crear un constructor
         Dht11() para actualizar los datos'''

        return str(self.__temperature)

    def get_humidity(self):
        '''Devuleve el valor de la humedad en %. Es necesario crear un constructor
        para actualizar los datos'''

        return str(self.__humidity)
