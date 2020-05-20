from Sensores import Sensores
from GeneradorJson import GeneradorJson
import time
import shlex, subprocess

datos = "sin datos"


class Main:
    while True:
        sensores = Sensores()
        temperaturaStr = sensores.getTemperature()
        humedadStr = sensores.getHumidity()
        fechaStr = sensores.getTimeNow()

        generador = GeneradorJson(temperaturaStr, humedadStr, fechaStr)
        generador.escribirJson()

        command_line = 'chromium-browser http://localhost:8082/'
        args = shlex.split(command_line)
        subprocess.run(args)

        time.sleep(3500.0)

        command_line2 = 'pkill -o chromium'
        args2 = shlex.split(command_line2)
        subprocess.run(args2)

        time.sleep(99.0)