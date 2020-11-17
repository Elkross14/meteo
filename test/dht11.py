import Adafruit_DHT
import time

sensor = Adafruit_DHT.DHT22
pin = 18


class Sensores:

    # constructor
    def __init__(self):
        self.__humidity, self.__temperature = Adafruit_DHT.read_retry(
            sensor, pin)

    # methods
    def getTemperature(self):
        return str(self.__temperature)

    def getHumidity(self):
        return str(self.__humidity)


while True:

    objeto_sensor = Sensores()

    print("Temperatura: " + objeto_sensor.getTemperature() +
          "ºC" + " | Humedad: " + objeto_sensor.getHumidity() + "%")
    time.sleep(2)
