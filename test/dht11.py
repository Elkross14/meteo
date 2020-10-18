import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
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


objeto_sensor = Sensores()

print("Temperatura: " + objeto_sensor.getTemperature() + "ºC")
print("Humedad: " + objeto_sensor.getHumidity() + "%")
