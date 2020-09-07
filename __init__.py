from sensor_dht11 import Dht11
import time
import os

datos = "sin datos"


class Main:
    sensores = Dht11()
    temperaturaStr = sensores.getTemperature()
    humedadStr = sensores.getHumidity()
    fechaStr = sensores.getTimeNow()

    link = "http://pabloduran.es/recibirdatos/{}/{}/{}".format(
        temperaturaStr, humedadStr, fechaStr)

    command_line = 'DISPLAY=:0 chromium-browser ' + link

    os.system(command_line)
