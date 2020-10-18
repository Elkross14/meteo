# datetime nos porporcionará la fecha de lectura
from datetime import datetime

from sensor_dht11 import Dht11
from sensor_bmp180 import Bmp180
from sensor_tsl2561 import Tsl2561
from sensor_velocidad_viento import VelocidadViento

from apscheduler.schedulers.background import BackgroundScheduler


class Main:
    '''Hace todas las llamadas a los sensores y envia los datos al
    servidor'''

    def __init__(self):

        # sensor de velocidad del viento
        self.objeto_sensor_viento = VelocidadViento()

        scheda = BackgroundScheduler()
        # scheda.add_job(self.iniciar_ciclo, 'cron', minute='40')
        scheda.add_job(self.iniciar_ciclo, 'interval', seconds=60)
        scheda.start()

    def iniciar_ciclo(self):
        '''Coge la fecha de lectura y hace las llamadas para leer los sensores'''

        fecha_lectura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("fecha: " + fecha_lectura)
        self.leer_dht11()
        self.leer_bmp180()
        self.leer_tsl2561()
        # self.leer_viento()

    @classmethod
    def leer_dht11(cls):
        '''Crea el objeto del sensor Dht11 y recoge la temperatura y humedad'''

        objeto_dht11 = Dht11()

        temperatura_str = objeto_dht11.get_temperature()
        humedad_str = objeto_dht11.get_humidity()

        print("-----------Dht11-----------")
        print("Temperatura:" + temperatura_str + "ºC")
        print("Humedad: " + humedad_str + "%")

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

    def leer_viento(self):
        '''Lee la velocidad máxima de racha y la velocidad media del viento.'''

        self.objeto_sensor_viento.calcularVelocidadMedia()

        vel_media_str = self.objeto_sensor_viento.getVelMedia()
        vel_racha_str = self.objeto_sensor_viento.getVelMaxRacha()

        print("----------Anemómetro----------")
        print("Velocidad Media: " + vel_media_str + " Km/H" +
              "\nVelocidad Racha: " + vel_racha_str + " Km/H")


meteo = Main()
