from datetime import datetime
import os
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler

from sensor_sht31 import Sht31
from sensor_mq2 import MQ2
from sensor_mq3 import MQ3
from sensor_mq4 import MQ4
from sensor_mq5 import MQ5
from sensor_mq7 import MQ7
from sensor_mq8 import MQ8
from sensor_mq9 import MQ9
from sensor_mq135 import MQ135

DOMINIO = "http://pabloduran.test/recibirMeteo/"
CLAVE_SERVIDOR = "4hdaH24bqQIPjufZYKJL" + "/"


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
        self.objeto_sensor_mq2 = MQ2()
        self.objeto_sensor_mq3 = MQ3()
        self.objeto_sensor_mq4 = MQ4()
        self.objeto_sensor_mq5 = MQ5()
        self.objeto_sensor_mq7 = MQ7()
        self.objeto_sensor_mq8 = MQ8()
        self.objeto_sensor_mq9 = MQ9()
        self.objeto_sensor_mq135 = MQ135()

        # Inicia la recogida de datos y envío cada hora
        scheda = BackgroundScheduler()
        # cheda.add_job(self.iniciar_ciclo, 'cron', minute='00')
        scheda.add_job(self.iniciar_ciclo, 'interval', seconds=10)
        scheda.start()

    def iniciar_ciclo(self):
        '''Recoge los datos de los sensores y envía los datos al servidor'''

        link = self.recoger_datos()

    def recoger_datos(self):
        '''Recoge los datos de todos los sensores y los devuelve en una cadena
        junto a la fecha.'''

        link = DOMINIO + CLAVE_SERVIDOR

        link += self.leer_fecha() + "?"
        link += self.leer_sht31(0x44)  # Temperatura ambiental
        link += "&" + self.leer_sht31(0x45)  # Temperatura caja de gases
        link += "&" + self.leer_mq2()
        link += "&" + self.leer_mq3()
        link += "&" + self.leer_mq4()
        link += "&" + self.leer_mq5()
        link += "&" + self.leer_mq7()
        link += "&" + self.leer_mq8()
        link += "&" + self.leer_mq9()
        link += "&" + self.leer_mq135()

        print(link)

        return link

    @classmethod
    def leer_fecha(cls):
        '''Lee la fecha del sistema'''

        fecha_lectura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(" ")
        print("fecha: " + fecha_lectura)

        return fecha_lectura.replace(" ", "%20")

    @classmethod
    def leer_sht31(cls, address):
        '''Lee los datos del sensor sht31'''

        objeto_sht31 = Sht31(address)

        if (address == 0x44):
            temperatura = "temperaturaSHT31=" + objeto_sht31.get_temperatura()
            humedad = "humedadSHT31=" + objeto_sht31.get_humedad()
        else:
            temperatura = "temperaturaSHT31gas=" + objeto_sht31.get_temperatura()
            humedad = "humedadSHT31gas=" + objeto_sht31.get_humedad()

        del objeto_sht31

        return temperatura + "&" + humedad

    def leer_mq2(self):
        '''Lee los datos del sensor mq2'''
        print("mq2")
        datos = ""

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq2.get_funcionamiento()):

            self.objeto_sensor_mq2.finalizar_ciclo()

            datos = "hidrogenoMQ2=" + self.objeto_sensor_mq2.get_hidrogeno()
            datos += "&metanoMQ2=" + self.objeto_sensor_mq2.get_metano()
            datos += "&gplMQ2=" + self.objeto_sensor_mq2.get_gpl()
            datos += "&propanoMQ2=" + self.objeto_sensor_mq2.get_propano()
            datos += "&alcoholMQ2=" + self.objeto_sensor_mq2.get_alcohol()
            datos += "&humoMQ2=" + self.objeto_sensor_mq2.get_humo()
            datos += "&alarmaMQ2=" + self.objeto_sensor_mq2.get_alarma()
            datos += "&voltajeMQ2=" + self.objeto_sensor_mq2.get_voltaje()

        else:  # El sensor no funciona
            datos = "funcionamientoMQ2=False"

            del self.objeto_sensor_mq2

            self.objeto_sensor_mq2 = MQ2()

        return datos

    def leer_mq3(self):
        '''Lee los datos del sensor mq3'''
        print("mq3")
        datos = ""

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq3.get_funcionamiento()):

            self.objeto_sensor_mq3.finalizar_ciclo()

            datos = "alcoholMQ3=" + self.objeto_sensor_mq3.get_alcohol()
            datos += "&bencenoMQ3=" + self.objeto_sensor_mq3.get_benceno()
            datos += "&alarmaMQ3=" + self.objeto_sensor_mq3.get_alarma()
            datos += "&voltajeMQ3=" + self.objeto_sensor_mq3.get_voltaje()

        else:  # El sensor no funciona
            datos = "funcionamientoMQ3=False"

            del self.objeto_sensor_mq3

            self.objeto_sensor_mq3 = MQ3()

        return datos

    def leer_mq4(self):
        '''Lee los datos del sensor mq4'''
        print("mq4")
        datos = ""

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq4.get_funcionamiento()):

            self.objeto_sensor_mq4.finalizar_ciclo()

            datos = "metanoMQ4=" + self.objeto_sensor_mq4.get_metano()
            datos += "&gplMQ4=" + self.objeto_sensor_mq4.get_gpl()
            datos += "&alarmaMQ4=" + self.objeto_sensor_mq4.get_alarma()
            datos += "&voltajeMQ4=" + self.objeto_sensor_mq4.get_voltaje()

        else:  # El sensor no funciona
            datos = "funcionamientoMQ4=False"

            del self.objeto_sensor_mq4

            self.objeto_sensor_mq4 = MQ4()

        return datos

    def leer_mq5(self):
        '''Lee los datos del sensor mq5'''
        print("mq5")
        datos = ""

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq5.get_funcionamiento()):

            self.objeto_sensor_mq5.finalizar_ciclo()

            datos = "gplMQ5=" + self.objeto_sensor_mq5.get_gpl()
            datos += "&metanoMQ5=" + self.objeto_sensor_mq5.get_metano()
            datos += "&alarmaMQ5=" + self.objeto_sensor_mq5.get_alarma()
            datos += "&voltajeMQ5=" + self.objeto_sensor_mq5.get_voltaje()

        else:  # El sensor no funciona
            datos = "funcionamientoMQ5=False"

            del self.objeto_sensor_mq5

            self.objeto_sensor_mq5 = MQ5()

        return datos

    def leer_mq7(self):
        '''Lee los datos del sensor mq7'''
        print("mq7")
        datos = ""

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq7.get_funcionamiento()):

            self.objeto_sensor_mq7.finalizar_ciclo()

            datos = "hidrogenoMQ7=" + self.objeto_sensor_mq7.get_hidrogeno()
            datos += "&coMQ7=" + self.objeto_sensor_mq7.get_co()
            datos += "&alarmaMQ7=" + self.objeto_sensor_mq7.get_alarma()
            datos += "&voltajeMQ7=" + self.objeto_sensor_mq7.get_voltaje()

        else:  # El sensor no funciona
            datos = "funcionamientoMQ7=False"

            del self.objeto_sensor_mq7

            self.objeto_sensor_mq7 = MQ7()

        return datos

    def leer_mq8(self):
        '''Lee los datos del sensor mq8'''
        print("mq8")
        datos = ""

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq8.get_funcionamiento()):

            self.objeto_sensor_mq8.finalizar_ciclo()

            datos = "hidrogenoMQ8=" + self.objeto_sensor_mq8.get_hidrogeno()
            datos += "&alarmaMQ8=" + self.objeto_sensor_mq8.get_alarma()
            datos += "&voltajeMQ8=" + self.objeto_sensor_mq8.get_voltaje()

        else:  # El sensor no funciona
            datos = "funcionamientoMQ8=False"

            del self.objeto_sensor_mq8

            self.objeto_sensor_mq8 = MQ8()

        return datos

    def leer_mq9(self):
        '''Lee los datos del sensor mq9'''
        print("mq9")
        datos = ""

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq9.get_funcionamiento()):

            self.objeto_sensor_mq9.finalizar_ciclo()

            datos = "coMQ9=" + self.objeto_sensor_mq9.get_co()
            datos += "&gplMQ9=" + self.objeto_sensor_mq9.get_gpl()
            datos += "&alarmaMQ9=" + self.objeto_sensor_mq9.get_alarma()
            datos += "&voltajeMQ9=" + self.objeto_sensor_mq9.get_voltaje()

        else:  # El sensor no funciona
            datos = "funcionamientoMQ9=False"

            del self.objeto_sensor_mq9

            self.objeto_sensor_mq9 = MQ9()

        return datos

    def leer_mq135(self):
        '''Lee los datos del sensor mq135'''
        print("mq135")
        datos = ""

        # Comprueba si el sensor funciona
        if(self.objeto_sensor_mq135.get_funcionamiento()):

            self.objeto_sensor_mq135.finalizar_ciclo()

            datos = "acetonaMQ135=" + self.objeto_sensor_mq135.get_acetona()
            datos += "&toluenoMQ135=" + self.objeto_sensor_mq135.get_tolueno()
            datos += "&alcoholMQ135=" + self.objeto_sensor_mq135.get_alcohol()
            datos += "&alarmaMQ135=" + self.objeto_sensor_mq135.get_alarma()
            datos += "&voltajeMQ135=" + self.objeto_sensor_mq135.get_voltaje()

        else:  # El sensor no funciona
            datos = "funcionamientoMQ135=False"

            del self.objeto_sensor_mq135

            self.objeto_sensor_mq135 = MQ135()

        return datos


meteo = Main()

while True:
    time.sleep(10)
