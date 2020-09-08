import Adafruit_DHT
from datetime import datetime

sensor = Adafruit_DHT.DHT11
pin = 17


class Dht11:

    def __init__(self):
        self.__humidity, self.__temperature = Adafruit_DHT.read_retry(
            sensor, pin)

    def getTemperature(self):
        return str(self.__temperature)

    def getHumidity(self):
        return str(self.__humidity)
