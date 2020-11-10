import os
import time

while True:

    command_line = 'firefox pabloduran.es/recibirdatos &'
    
    os.system(command_line)

    print("esperando")

    time.sleep(250)

    print('cerrando navegador')

    command_line = 'pkill -f firefox'

    os.system(command_line)

    time.sleep(50)
