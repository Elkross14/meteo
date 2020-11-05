from datetime import datetime
import os
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

from sensor_dht11 import Dht11
from sensor_bmp180 import Bmp180
from sensor_tsl2561 import Tsl2561
from sensor_veleta import Veleta
from sensor_velocidad_viento import VelocidadViento
from sensor_lluvia import Pluviometro


class Main:
    '''Hace todas las llamadas a los sensores y envia los datos al
    servidor'''

    def __init__(self):

        atexit.register(print, "Program exited successfully!")

        # iniciamos anemometro y pluviometro para que recogan datos
        # hasta la la siguiente hora a las 00 minutos.
        self.objeto_sensor_viento = VelocidadViento()
        self.objeto_sensor_lluvia = Pluviometro()

        self.iniciar_ciclo()

        scheda = BackgroundScheduler()
        # scheda.add_job(self.iniciar_ciclo, 'cron', minute='40')
        scheda.add_job(self.iniciar_ciclo, 'interval', seconds=60)
        scheda.start()

    def iniciar_ciclo(self):
        '''Coge la fecha de lectura y hace las llamadas para leer los sensores'''

        link = self.recoger_datos()

        self.enviar_datos(link)

    def recoger_datos(self):
        '''Recoge los datos de todos los sensores y los devuelve en una cadena
        junto a la fecha.'''

        fecha = dht11 = bmp180 = tsl2561 = viento = lluvia = "100"
        direc = "None"

        fecha = self.leer_fecha()
        dht11 = self.leer_dht11()
        bmp180 = self.leer_bmp180()
        tsl2561 = self.leer_tsl2561()
        direc = self.leer_direccion_viento()
        viento = self.leer_viento()
        lluvia = self.leer_lluvia()

        link = fecha + "/" + dht11 + "/" + bmp180 + "/" + \
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
    def leer_dht11(cls):
        '''Crea el objeto del sensor Dht11 y recoge la temperatura y humedad'''

        objeto_dht11 = Dht11()

        temperatura_str = objeto_dht11.get_temperature()
        humedad_str = objeto_dht11.get_humidity()

        print("-----------Dht11-----------")
        print("Temperatura: " + temperatura_str + "ºC")
        print("Humedad: " + humedad_str + "%")

        return temperatura_str + "/" + humedad_str

    @classmethod
    def leer_bmp180(cls):
        '''Crea el objeto del sensor Bmp180 y recoge la presión, temperatura
        y altura'''

        objeto_bmp180 = Bmp180()

        presion_str = objeto_bmp180.get_presion()
        temperatura_str = objeto_bmp180.get_temperatura()
        altura_str = objeto_bmp180.get_altura()

        print("-----------Bmp180----------")
        print("Presión: " + presion_str + "hPa")
        print("Tempreratura: " + temperatura_str + "ºC")
        print("Altura: " + altura_str + "m")

        return temperatura_str + "/" + presion_str + "/" + altura_str

    @classmethod
    def leer_tsl2561(cls):
        '''Crea un objeto del sensor Tsl2561 y recoge la luz total, luz infrarroja
        y luz visible'''

        objeto_tsl2561 = Tsl2561()

        luz_total_str = objeto_tsl2561.get_luz_total()
        luz_infrarroja_str = objeto_tsl2561.get_luz_infrarroja()
        luz_visible_str = objeto_tsl2561.get_luz_visible()

        print("----------Tsl2561----------")
        print("Luz total: " + luz_total_str + "Lux")
        print("Luz infrarroja: " + luz_infrarroja_str + "Lux")
        print("Luz visible: " + luz_visible_str + "Lux")

        return luz_infrarroja_str + "/" + luz_visible_str + "/" + luz_total_str

    @classmethod
    def leer_direccion_viento(cls):
        '''Lee la dirección del viento.'''

        objeto_veleta = Veleta()

        direccion_viento = objeto_veleta.get_direccion_viento()

        print("----------Veleta----------")
        print("Dirección del viento: " + direccion_viento)

        return direccion_viento

    def leer_viento(self):
        '''Lee la velocidad máxima de racha y la velocidad media del viento.'''

        self.objeto_sensor_viento.calcular_velocidad_media()
        self.objeto_sensor_viento.reiniciar_valores()

        vel_media_str = self.objeto_sensor_viento.get_vel_media()
        vel_racha_str = self.objeto_sensor_viento.get_vel_max_racha()

        print("----------Anemómetro----------")
        print("Velocidad Media: " + vel_media_str + " Km/H" +
              "\nVelocidad Racha: " + vel_racha_str + " Km/H")

        return vel_media_str + "/" + vel_racha_str

    def leer_lluvia(self):
        '''Lee la cantidad de litros por metro cuadrado que ha llovido'''

        self.objeto_sensor_lluvia.calcular_lluvia()
        self.objeto_sensor_lluvia.reiniciar_valores()

        lluvia = self.objeto_sensor_lluvia.get_litros()

        print("----------Pluviometro----------")
        print("LLuvia: " + lluvia + " L/m3")

        return lluvia

    def enviar_datos(self, link):
        '''Le pasamos el link con los datos a enviar al servidor.
        Abre una ventana del navegador y escribe la URL.'''

        url = "pabloduran.es/recibirdatos/hYlkg6Io/" + link
        print("URL: " + url)

        command_line = 'DISPLAY=:0 firefox ' + url + ' &'

        os.system(command_line)


meteo = Main()

input()
