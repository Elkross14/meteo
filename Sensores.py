import Adafruit_DHT
from datetime import datetime

sensor = Adafruit_DHT.DHT11
pin = 17


class Sensores:

    def __init__(self):
        self.__humidity, self.__temperature = Adafruit_DHT.read_retry(sensor, pin)
        self.timeDate = datetime.now()

    def getTemperature(self):
        return str(self.__temperature)

    def getHumidity(self):
        return str(self.__humidity)

    def getTimeNow(self):
        fecha = self.timeDate.strftime("%Y-%m-%d %H:%M:%S")
        return fecha.replace(" ", "%20")