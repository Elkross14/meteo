from datetime import datetime
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler

from acceso_web import AccesoWeb
import requests

from sensor_sht31 import Sht31
from sensor_bmp180 import Bmp180
from sensor_bmp280 import Bmp280
from sensor_tsl2561 import Tsl2561
from sensor_veleta import Veleta
from sensor_velocidad_viento import VelocidadViento
from sensor_lluvia import Pluviometro
from sensor_mq2 import MQ2
from sensor_mq3 import MQ3
from sensor_mq4 import MQ4
from sensor_mq5 import MQ5
from sensor_mq7 import MQ7
from sensor_mq8 import MQ8
from sensor_mq9 import MQ9
from sensor_mq135 import MQ135


class Main:
    '''Hace todas las llamadas a los sensores y envia los datos al
    servidor'''

    def __init__(self):

        # nos guarda toda la información de lo ocurridoe en el programa
        logging.basicConfig(filename='registro.log',
                            level=logging.ERROR,
                            format='%(asctime)s %(message)s')

        self.llamar_constructores()

        # Inicia la recogida de datos y envío cada hora
        scheda = BackgroundScheduler()
        scheda.add_job(self.iniciar_ciclo, 'cron', minute='00')
        scheda.start()

    def llamar_constructores(self):
        '''Llama a los constructores de los sensores que tienen que hacer
        lectura continua durante todo el ciclo.'''

        tiempo = 2

        self.objeto_sensor_viento = VelocidadViento()
        time.sleep(tiempo)
        self.objeto_sensor_lluvia = Pluviometro()
        time.sleep(tiempo)
        self.objeto_sensor_mq2 = MQ2()
        time.sleep(tiempo)
        self.objeto_sensor_mq3 = MQ3()
        time.sleep(tiempo)
        self.objeto_sensor_mq4 = MQ4()
        time.sleep(tiempo)
        self.objeto_sensor_mq5 = MQ5()
        time.sleep(tiempo)
        self.objeto_sensor_mq7 = MQ7()
        time.sleep(tiempo)
        self.objeto_sensor_mq8 = MQ8()
        time.sleep(tiempo)
        self.objeto_sensor_mq9 = MQ9()
        time.sleep(tiempo)
        self.objeto_sensor_mq135 = MQ135()

    def iniciar_ciclo(self):
        '''Recoge los datos de los sensores y envía los datos al servidor'''

        acceso_web = AccesoWeb()

        link = acceso_web.get_dominio() + acceso_web.get_clave_servidor()
        link += self.leer_fecha()

        datos = self.recoger_datos()

        self.enviar_datos(link, datos)

    def recoger_datos(self):
        '''Recoge los datos de todos los sensores y los devuelve en un json.'''

        datos = {}
        datos = {**datos, **self.leer_sht31(0x44)}  # Temperatura ambiental
        #datos = {**datos, **self.leer_bmp180()}
        #datos = {**datos, **self.leer_bmp280()}
        datos = {**datos, **self.leer_tsl2561()}
        datos = {**datos, **self.leer_direccion_viento()}
        datos = {**datos, **self.leer_viento()}
        datos = {**datos, **self.leer_lluvia()}
        datos = {**datos, **self.leer_sht31(0x45)}  # Temperatura caja de gases
        datos = {**datos, **self.leer_mq2()}
        datos = {**datos, **self.leer_mq3()}
        datos = {**datos, **self.leer_mq4()}
        datos = {**datos, **self.leer_mq5()}
        datos = {**datos, **self.leer_mq7()}
        datos = {**datos, **self.leer_mq8()}
        datos = {**datos, **self.leer_mq9()}
        datos = {**datos, **self.leer_mq135()}

        return datos

    @classmethod
    def leer_fecha(cls):
        '''Lee la fecha del sistema'''

        fecha_lectura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return fecha_lectura.replace(" ", "%20")

    @classmethod
    def leer_sht31(cls, address):
        '''Lee los datos del sensor sht31'''

        datos = {}

        objeto_sht31 = Sht31(address)

        if (address == 0x44):

            datos["temperaturaSHT31"] = objeto_sht31.get_temperatura()
            datos["humedadSHT31"] = objeto_sht31.get_humedad()

        else:

            datos["temperaturaSHT31gas"] = objeto_sht31.get_temperatura()
            datos["humedadSHT31gas"] = objeto_sht31.get_humedad()

        del objeto_sht31

        return datos

    @classmethod
    def leer_bmp180(cls):
        '''Crea el objeto del sensor Bmp180 y recoge la presión, temperatura
        y altura'''

        datos = {}

        objeto_bmp180 = Bmp180()

        datos["presionBMP180"] = objeto_bmp180.get_presion()
        datos["temperaturaBMP180"] = objeto_bmp180.get_temperatura()
        datos["alturaBMP180"] = objeto_bmp180.get_altura()

        return datos

    @classmethod
    def leer_bmp280(cls):
        '''Crea el objeto del sensor Bmp280 y recoge la presión, temperatura
        y altura'''

        datos = {}

        objeto_bmp280 = Bmp280()

        datos["presionBMP180"] = objeto_bmp280.get_presion()
        datos["temperaturaBMP180"] = objeto_bmp280.get_temperatura()

        return datos

    @classmethod
    def leer_tsl2561(cls):
        '''Crea un objeto del sensor Tsl2561 y recoge la luz total, luz infrarroja
        y luz visible'''

        datos = {}

        objeto_tsl2561 = Tsl2561()

        datos["luzTotalTSL2561"] = objeto_tsl2561.get_luz_total()
        datos["luzInfrarrojaTSL2561"] = objeto_tsl2561.get_luz_infrarroja()
        datos["luzVisibleTSL2561"] = objeto_tsl2561.get_luz_visible()

        return datos

    @classmethod
    def leer_direccion_viento(cls):
        '''Lee la dirección del viento.'''

        datos = {}

        objeto_veleta = Veleta()

        if(objeto_veleta.get_funcionamiento()):

            datos["direccionVeleta"] = objeto_veleta.get_direccion()

        else:  # El sensor no funciona
            datos["funcionamientoVeleta"] = False

        del objeto_veleta

        return datos

    def leer_viento(self):
        '''Lee la velocidad máxima de racha y la velocidad media del viento.'''

        datos = {}

        self.objeto_sensor_viento.finalizar_ciclo()

        datos["velMediaViento"] = self.objeto_sensor_viento.get_vel_media()
        datos["velRachaViento"] = self.objeto_sensor_viento.get_vel_max_racha()

        return datos

    def leer_lluvia(self):
        '''Lee la cantidad de litros por metro cuadrado que ha llovido'''

        datos = {}

        self.objeto_sensor_lluvia.calcular_lluvia()
        self.objeto_sensor_lluvia.reiniciar_valores()

        datos["lluvia"] = self.objeto_sensor_lluvia.get_litros()

        return datos

    def leer_mq2(self):
        '''Lee los datos del sensor mq2'''

        datos = {}

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq2.get_funcionamiento()):

            self.objeto_sensor_mq2.finalizar_ciclo()

            datos["hidrogenoMQ2"] = self.objeto_sensor_mq2.get_hidrogeno()
            datos["metanoMQ2"] = self.objeto_sensor_mq2.get_metano()
            datos["gplMQ2"] = self.objeto_sensor_mq2.get_gpl()
            datos["propanoMQ2"] = self.objeto_sensor_mq2.get_propano()
            datos["alcoholMQ2"] = self.objeto_sensor_mq2.get_alcohol()
            datos["humoMQ2"] = self.objeto_sensor_mq2.get_humo()
            datos["alarmaMQ2"] = self.objeto_sensor_mq2.get_alarma()
            datos["voltajeMQ2"] = self.objeto_sensor_mq2.get_voltaje()

        else:  # El sensor no funciona
            datos["funcionamientoMQ2"] = False

            del self.objeto_sensor_mq2

            self.objeto_sensor_mq2 = MQ2()

        return datos

    def leer_mq3(self):
        '''Lee los datos del sensor mq3'''

        datos = {}

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq3.get_funcionamiento()):

            self.objeto_sensor_mq3.finalizar_ciclo()

            datos["alcoholMQ3"] = self.objeto_sensor_mq3.get_alcohol()
            datos["bencenoMQ3"] = self.objeto_sensor_mq3.get_benceno()
            datos["alarmaMQ3"] = self.objeto_sensor_mq3.get_alarma()
            datos["voltajeMQ3"] = self.objeto_sensor_mq3.get_voltaje()

        else:  # El sensor no funciona
            datos["funcionamientoMQ3"] = False

            del self.objeto_sensor_mq3

            self.objeto_sensor_mq3 = MQ3()

        return datos

    def leer_mq4(self):
        '''Lee los datos del sensor mq4'''

        datos = {}

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq4.get_funcionamiento()):

            self.objeto_sensor_mq4.finalizar_ciclo()

            datos["metanoMQ4"] = self.objeto_sensor_mq4.get_metano()
            datos["gplMQ4"] = self.objeto_sensor_mq4.get_gpl()
            datos["alarmaMQ4"] = self.objeto_sensor_mq4.get_alarma()
            datos["voltajeMQ4"] = self.objeto_sensor_mq4.get_voltaje()

        else:  # El sensor no funciona
            datos["funcionamientoMQ4"] = False

            del self.objeto_sensor_mq4

            self.objeto_sensor_mq4 = MQ4()

        return datos

    def leer_mq5(self):
        '''Lee los datos del sensor mq5'''

        datos = {}

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq5.get_funcionamiento()):

            self.objeto_sensor_mq5.finalizar_ciclo()

            datos["gplMQ5"] = self.objeto_sensor_mq5.get_gpl()
            datos["metanoMQ5"] = self.objeto_sensor_mq5.get_metano()
            datos["alarmaMQ5"] = self.objeto_sensor_mq5.get_alarma()
            datos["voltajeMQ5"] = self.objeto_sensor_mq5.get_voltaje()

        else:  # El sensor no funciona
            datos["funcionamientoMQ5"] = False

            del self.objeto_sensor_mq5

            self.objeto_sensor_mq5 = MQ5()

        return datos

    def leer_mq7(self):
        '''Lee los datos del sensor mq7'''

        datos = {}

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq7.get_funcionamiento()):

            self.objeto_sensor_mq7.finalizar_ciclo()

            datos["hidrogenoMQ7"] = self.objeto_sensor_mq7.get_hidrogeno()
            datos["coMQ7"] = self.objeto_sensor_mq7.get_co()
            datos["alarmaMQ7"] = self.objeto_sensor_mq7.get_alarma()
            datos["voltajeMQ7"] = self.objeto_sensor_mq7.get_voltaje()

        else:  # El sensor no funciona
            datos["funcionamientoMQ7"] = False

            del self.objeto_sensor_mq7

            self.objeto_sensor_mq7 = MQ7()

        return datos

    def leer_mq8(self):
        '''Lee los datos del sensor mq8'''

        datos = {}

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq8.get_funcionamiento()):

            self.objeto_sensor_mq8.finalizar_ciclo()

            datos["hidrogenoMQ8"] = self.objeto_sensor_mq8.get_hidrogeno()
            datos["alarmaMQ8"] = self.objeto_sensor_mq8.get_alarma()
            datos["voltajeMQ8"] = self.objeto_sensor_mq8.get_voltaje()

        else:  # El sensor no funciona
            datos["funcionamientoMQ8"] = False

            del self.objeto_sensor_mq8

            self.objeto_sensor_mq8 = MQ8()

        return datos

    def leer_mq9(self):
        '''Lee los datos del sensor mq9'''

        datos = {}

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq9.get_funcionamiento()):

            self.objeto_sensor_mq9.finalizar_ciclo()

            datos["coMQ9"] = self.objeto_sensor_mq9.get_co()
            datos["gplMQ9"] = self.objeto_sensor_mq9.get_gpl()
            datos["alarmaMQ9"] = self.objeto_sensor_mq9.get_alarma()
            datos["voltajeMQ9"] = self.objeto_sensor_mq9.get_voltaje()

        else:  # El sensor no funciona
            datos["funcionamientoMQ9"] = False

            del self.objeto_sensor_mq9

            self.objeto_sensor_mq9 = MQ9()

        return datos

    def leer_mq135(self):
        '''Lee los datos del sensor mq135'''

        datos = {}

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq135.get_funcionamiento()):

            self.objeto_sensor_mq135.finalizar_ciclo()

            datos["acetonaMQ135"] = self.objeto_sensor_mq135.get_acetona()
            datos["toluenoMQ135"] = self.objeto_sensor_mq135.get_tolueno()
            datos["alcoholMQ135"] = self.objeto_sensor_mq135.get_alcohol()
            datos["alarmaMQ135"] = self.objeto_sensor_mq135.get_alarma()
            datos["voltajeMQ135"] = self.objeto_sensor_mq135.get_voltaje()

        else:  # El sensor no funciona
            datos["funcionamientoMQ135"] = False

            del self.objeto_sensor_mq135

            self.objeto_sensor_mq135 = MQ135()

        return datos

    def enviar_datos(self, link, datos):
        '''Envia los datos al servidor'''

        logging.debug(datos)
        requests.get(link, params=datos, timeout=300)


meteo = Main()

while True:
    time.sleep(10)
