from datetime import datetime
import os
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler

from sensor_dht22 import Dht22
from sensor_bmp180 import Bmp180
from sensor_tsl2561 import Tsl2561
from sensor_veleta import Veleta
from sensor_velocidad_viento import VelocidadViento
from sensor_lluvia import Pluviometro


class Main:
    '''Hace todas las llamadas a los sensores y envia los datos al
    servidor'''

    def __init__(self):

        # nos guarda toda la información de lo ocurridoe en el programa
        logging.basicConfig(filename='registro.log',
                            level=logging.INFO,
                            format='%(asctime)s %(message)s')

        # iniciamos anemometro y pluviometro para que recojan datos
        # hasta la la siguiente hora a las 00 minutos.
        self.objeto_sensor_viento = VelocidadViento()
        self.objeto_sensor_lluvia = Pluviometro()

        # Inicia la recogida de datos y envío cada hora
        scheda = BackgroundScheduler()
        scheda.add_job(self.iniciar_ciclo, 'cron', minute='00')
        scheda.start()

    def iniciar_ciclo(self):
        '''Recoge los datos de los sensores y envía los datos al servidor'''

        link = self.recoger_datos()

        self.enviar_datos(link)

        time.sleep(1800)

        self.cerrar_navegador()

    def recoger_datos(self):
        '''Recoge los datos de todos los sensores y los devuelve en una cadena
        junto a la fecha.'''

        fecha = self.leer_fecha()
        # dht22 = self.leer_dht22()
        dht22 = "0/0"
        bmp180 = self.leer_bmp180()
        tsl2561 = self.leer_tsl2561()
        direc = self.leer_direccion_viento()
        viento = self.leer_viento()
        lluvia = self.leer_lluvia()

        link = fecha + "/" + dht22 + "/" + bmp180 + "/" + \
            tsl2561 + "/" + viento + "/" + direc + "/" + lluvia

        return link

    @classmethod
    def leer_fecha(cls):
        '''Lee la fecha del sistema'''

        fecha_lectura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(" ")
        print("fecha: " + fecha_lectura)

        return fecha_lectura.replace(" ", "%20")

    @classmethod
    def leer_dht22(cls):
        '''Crea el objeto del sensor Dht22 y recoge la temperatura y humedad'''

        objeto_dht22 = Dht22()

        temperatura_str = objeto_dht22.get_temperature()
        humedad_str = objeto_dht22.get_humidity()

        return temperatura_str + "/" + humedad_str

    @classmethod
    def leer_bmp180(cls):
        '''Crea el objeto del sensor Bmp180 y recoge la presión, temperatura
        y altura'''

        objeto_bmp180 = Bmp180()

        presion_str = objeto_bmp180.get_presion()
        temperatura_str = objeto_bmp180.get_temperatura()
        altura_str = objeto_bmp180.get_altura()

        logging.info('Datos del sensor BMP180 leidos correctamente')

        return temperatura_str + "/" + presion_str + "/" + altura_str

    @classmethod
    def leer_tsl2561(cls):
        '''Crea un objeto del sensor Tsl2561 y recoge la luz total, luz infrarroja
        y luz visible'''

        objeto_tsl2561 = Tsl2561()

        luz_total_str = objeto_tsl2561.get_luz_total()
        luz_infrarroja_str = objeto_tsl2561.get_luz_infrarroja()
        luz_visible_str = objeto_tsl2561.get_luz_visible()

        logging.info('Datos del sensor TSL2561 leidos correctamente')

        return luz_infrarroja_str + "/" + luz_visible_str + "/" + luz_total_str

    @classmethod
    def leer_direccion_viento(cls):
        '''Lee la dirección del viento.'''

        objeto_veleta = Veleta()

        direccion_viento = objeto_veleta.get_direccion_viento()

        logging.info('Dato de la veleta leido correctamente')

        return direccion_viento

    def leer_viento(self):
        '''Lee la velocidad máxima de racha y la velocidad media del viento.'''

        self.objeto_sensor_viento.calcular_velocidad_media()
        self.objeto_sensor_viento.reiniciar_valores()

        vel_media_str = self.objeto_sensor_viento.get_vel_media()
        vel_racha_str = self.objeto_sensor_viento.get_vel_max_racha()

        logging.info('Datos del anemómetro leidos correctamente')

        return vel_media_str + "/" + vel_racha_str

    def leer_lluvia(self):
        '''Lee la cantidad de litros por metro cuadrado que ha llovido'''

        self.objeto_sensor_lluvia.calcular_lluvia()
        self.objeto_sensor_lluvia.reiniciar_valores()

        lluvia = self.objeto_sensor_lluvia.get_litros()

        logging.info('Dato del pluviómetro leido correctamente')

        return lluvia

    def enviar_datos(self, link):
        '''Le pasamos el link con los datos a enviar al servidor.
        Abre una ventana del navegador y escribe la URL.'''

        url = "pabloduran.es/recibirdatos/hYlkg6Io/" + link
        print("URL: " + url)

        command_line = 'DISPLAY=:0 firefox ' + url + ' &'

        os.system(command_line)

    def cerrar_navegador(self):
        '''Cierra el navegado que se está usando para enviar los datos'''

        os.system("pkill firefox")


meteo = Main()

while True:
    time.sleep(10)
