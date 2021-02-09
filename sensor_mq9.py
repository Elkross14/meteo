# I2C comunicación
import board
import busio

# librerías del ADC ADS1115
import adafruit_ads1x15.ads1115 as ads1115
from adafruit_ads1x15.analog_in import AnalogIn

# lectura digital
from gpiozero import Button

# Medición por intervalos
from apscheduler.schedulers.background import BackgroundScheduler

# Calcular PPM
from calculos_gas import Calculos

# para registro de errores
import logging


# direccion I2C del ADS11115
ADDRESS = 0x4a  # pin address conectado a VDD
PIN = 2  # canal analógico del chip

alarma_mq9 = 0


class MQ9:
    """Detector de gas MQ9"""

    # resistencia del sensor
    LOAD_RESISTANCE = 1

    # pin salida digital
    DOutput = Button(27)

    # Ro value of the sensor
    ro = 1.014

    # Curva logaritmica con base 10
    CO_CURVA = [2.301030, 0.227887, -0.478819]
    GPL_CURVA = [2.301030, 0.324282, -0.471955]

    # gas en ppm
    co_ppm = 0
    gpl_ppm = 0
    voltaje = 0
    funcionamiento = True

    # Contadores
    voltaje_acumulado = 0
    cantidad_muestras = 0

    def __init__(self, convertor=ads1115.ADS1115, pin=PIN, address=ADDRESS):
        '''Inicia con la lectura periodica de gases del sensor MQ9'''

        # Permique que el resto del programa sigua funcionando aunque el ADC no funcione
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            adc = convertor(i2c=i2c, address=address)

            self.channel = AnalogIn(adc, pin)

            self.sched_mq9 = BackgroundScheduler()
            self.sched_mq9.add_job(self.leer_voltaje, 'interval',
                                   seconds=5, id="sched_mq9")
            self.sched_mq9.start()

        except (ValueError, OSError):
            self.funcionamiento = False

            logging.error('El ADC del MQ9 ha dejado de funcionar.')

    def leer_voltaje(self):
        '''leerá el voltaje cada cierto tiempo y lo irá acumulando, además
        lleva la cuenta de cuantos ciclos de lectura lleva.'''

        # Evita que se rompa el programa en caso de que el ADC deje de funcionar a mitad
        # de una lectura de voltaje.
        try:
            self.voltaje_acumulado += self.channel.voltage
            self.cantidad_muestras += 1

        except (ValueError, OSError):
            self.funcionamiento = False
            logging.error('El ADC del MQ9 ha dejado de funcionar.')

            self.sched_mq9.remove_job("sched_mq9")

    def finalizar_ciclo(self):
        '''Llama a las funciones necesarias para finalizar el ciclo de lectura
        de datos y empezar uno nuevo'''

        self.calcular_concentracion()

        self.reiniciar_contadores()

    def calcular_concentracion(self):
        '''Hace los calculos necesarios para obtener las concentraciones
        de los gases en ppm'''

        calculos = Calculos()

        self.voltaje = calculos.calcular_voltaje(
            self.voltaje_acumulado, self.cantidad_muestras)

        rs = calculos.calcular_resistencia(self.voltaje, self.LOAD_RESISTANCE)

        ratio = rs / self.ro

        self.co_ppm = calculos.calcular_ppm(ratio, self.CO_CURVA)

        self.gpl_ppm = calculos.calcular_ppm(ratio, self.GPL_CURVA)

    def activar_alarma(self):
        '''Pasa la variable alarma a True en el caso de que el pin digital
        envien una señal.'''

        global alarma_mq9

        alarma_mq9 = 1

    def reiniciar_contadores(self):
        '''Reinicia los valores de los contadores para tomar nuevas lecturas.'''

        global alarma_mq9

        self.voltaje_acumulado = 0
        self.cantidad_muestras = 0
        alarma_mq9 = 0

    def get_co(self):
        '''Devuelve un string de la variable co_ppm con tres decimales'''

        return self.co_ppm

    def get_gpl(self):
        '''Devuelve un string de la variable gpl_ppm con tres decimales'''

        return self.gpl_ppm

    def get_alarma(self):
        '''Devuelve un String de la variable alarma'''

        global alarma_mq9

        return str(alarma_mq9)

    def get_voltaje(self):
        '''Devuelve un String de la variable voltaje'''

        return str(self.voltaje)

    def get_funcionamiento(self):
        '''Nos dice mediante un boolean si el sensor funciona. En el caso de True
        es que el sensor funciona'''

        return self.funcionamiento

    # cuando el sensor detecte una concentración peligrosa lanzará una alarma
    DOutput.when_pressed = activar_alarma
