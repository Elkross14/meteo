from Sensores import Sensores
import time
import os

datos = "sin datos"

class Main:
    sensores = Sensores()
    temperaturaStr = sensores.getTemperature()
    humedadStr = sensores.getHumidity()
    fechaStr = sensores.getTimeNow()
      
    link = "http://pabloduran.es/recibirdatos/{}/{}/{}".format(temperaturaStr, humedadStr, fechaStr)
    
    command_line = 'DISPLAY=:0 chromium-browser ' + link
    
    os.system(command_line)