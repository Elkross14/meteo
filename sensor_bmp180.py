import Adafruit_BMP.BMP085 as BMP085


class Bmp180:

    def __init__(self):
        sensor = BMP085.BMP085()

        self.atm = sensor.read_pressure() / 101325  # pasado de Pa a atm al leer el dato
        self.temperatura = sensor.read_temperature()
        self.altura = sensor.read_altitude()

    def getPresion(self):
        return str("{:.3f}".format(self.atm))

    def getTemperatura(self):
        return str("{:.3f}".format(self.temperatura))

    def getAltura(self):
        return str("{:.3f}".format(self.altura))
