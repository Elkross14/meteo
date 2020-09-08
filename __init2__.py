# datetime nos porporcionará la fecha de lectura
from datetime import datetime

from sensor_dht11 import Dht11
from sensor_bmp180 import Bmp180
from sensor_tsl2561 import Tsl2561
from sensor_velocidad_viento import VelocidadViento

from apscheduler.schedulers.background import BackgroundScheduler


class Main:

    # variables del sensor dht11
    dht11_temperatura_str = ""  # en ºC
    dht11_humedad_str = ""  # en %

    # variables del sensor bmp180
    bmp180_presion_str = ""  # en atm
    bmp180_temperatura_str = ""  # en ºC
    bmp180_altura_str = ""  # en metros

    # variables del sensor tsl2561
    luz_total_tsl2561_str = ""  # en lux
    luz_infrarroja_tsl2561_str = ""  # en lux
    luz_visible_tsl2561_str = ""  # en lux

    def __init__(self):

        self.inicialCiclo()

        # sensor de velocidad del viento
        objeto_sensor_viento = VelocidadViento()

        scheda = BackgroundScheduler()
        scheda.add_job(
            objeto_sensor_viento.calcularVelocidadMedia, 'cron', minute='*/30')
        scheda.start()

    # inicia la secuencia de recogida de datos y reseteo de variables
    def inicialCiclo(self):
        fecha_lectura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("fecha: " + fecha_lectura)
        self.leerDht11()
        self.leerBmp180()
        self.leerTsl2561()

    def leerDht11(self):
        global dht11_temperatura_str
        global dht11_humedad_str

        objeto_dht11 = Dht11()

        dht11_temperatura_str = objeto_dht11.getTemperature()
        dht11_humedad_str = objeto_dht11.getHumidity()

    def leerBmp180(self):
        global bmp180_presion_str
        global bmp180_temperatura_str
        global bmp180_altura_str

        objeto_bmp180 = Bmp180()

        bmp180_presion_str = objeto_bmp180.getPresion()
        bmp180_temperatura_str = objeto_bmp180.getTemperatura()
        bmp180_altura_str = objeto_bmp180.getAltura()

    def leerTsl2561(self):
        global luz_total_tsl2561_str
        global luz_infrarroja_tsl2561_str
        global luz_visible_tsl2561_str

        objeto_tsl2561 = Tsl2561()

        luz_total_tsl2561_str = objeto_tsl2561.getLuzTotal()
        luz_infrarroja_tsl2561_str = objeto_tsl2561.getLuzInfrarroja()
        luz_visible_tsl2561_str = objeto_tsl2561.getLuzVisible()


meteo = Main()
# meteo.inicialCiclo()
