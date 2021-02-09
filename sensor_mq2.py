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
ADDRESS = 0x49  # pin address conectado a VDD
PIN = 0  # canal analógico del chip

alarma_mq2 = 0


class MQ2:
    """Detector de gas MQ2"""

    # resistencia del sensor
    LOAD_RESISTANCE = 1

    # pin salida digital
    DOutput = Button(14)

    # Ro value of the sensor
    ro = 10.878

    # Curva logaritmica con base 10
    HIDROGENO_CURVA = [2.301030, 0.322219, -0.473054]
    METANO_CURVA = [2.301030, 0.484300, -0.379901]
    GPL_CURVA = [2.301030, 0.230449, -0.479982]
    PROPANO_CURVA = [2.301030, 0.250420, -0.472794]
    ALCOHOL_CURVA = [2.301030, 0.460898, -0.381398]
    HUMO_CURVA = [2.301030, 0.535294, -0.441423]

    # gas en ppm
    hidrogeno_ppm = 0
    metano_ppm = 0
    gpl_ppm = 0
    propano_ppm = 0
    alcohol_ppm = 0
    humo_ppm = 0
    voltaje = 0
    funcionamiento = True

    # Contadores
    voltaje_acumulado = 0
    cantidad_muestras = 0

    def __init__(self, convertor=ads1115.ADS1115, pin=PIN, address=ADDRESS):
        '''Inicia con la lectura periodica de gases del sensor MQ2'''

        # Permique que el resto del programa sigua funcionando aunque el ADC no funcione
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            adc = convertor(i2c=i2c, address=address)
            self.channel = AnalogIn(adc, pin)

            self.sched_mq2 = BackgroundScheduler()
            self.sched_mq2.add_job(self.leer_voltaje, 'interval',
                                   seconds=5, id="sched_mq2")
            self.sched_mq2.start()

        except (ValueError, OSError):
            self.funcionamiento = False

            logging.error('El ADC del MQ2 ha dejado de funcionar.')

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
            logging.error('El ADC del MQ2 ha dejado de funcionar.')

            self.sched_mq2.remove_job("sched_mq2")

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

        self.hidrogeno_ppm = calculos.calcular_ppm(ratio, self.HIDROGENO_CURVA)

        self.metano_ppm = calculos.calcular_ppm(ratio, self.METANO_CURVA)

        self.gpl_ppm = calculos.calcular_ppm(ratio, self.GPL_CURVA)

        self.propano_ppm = calculos.calcular_ppm(ratio, self.PROPANO_CURVA)

        self.alcohol_ppm = calculos.calcular_ppm(ratio, self.ALCOHOL_CURVA)

        self.humo_ppm = calculos.calcular_ppm(ratio, self.HUMO_CURVA)

    def activar_alarma(self):
        '''Pasa la variable alarma a True en el caso de que el pin digital
        envien una señal.'''

        global alarma_mq2

        alarma_mq2 = 1

    def reiniciar_contadores(self):
        '''Reinicia los valores de los contadores para tomar nuevas lecturas.'''

        global alarma_mq2

        self.voltaje_acumulado = 0
        self.cantidad_muestras = 0
        alarma_mq2 = 0

    def get_hidrogeno(self):
        '''Devuelve un string de la variable hidrogeno_ppm con tres decimales'''

        return self.hidrogeno_ppm

    def get_metano(self):
        '''Devuelve un string de la variable metano_ppm con tres decimales'''

        return self.metano_ppm

    def get_gpl(self):
        '''Devuelve un string de la variable gpl_ppm con tres decimales'''

        return self.gpl_ppm

    def get_propano(self):
        '''Devuelve un string de la variable propano_ppm con tres decimales'''

        return self.propano_ppm

    def get_alcohol(self):
        '''Devuelve un string de la variable alcohol_ppm con tres decimales'''

        return self.alcohol_ppm

    def get_humo(self):
        '''Devuelve un string de la variable humo_ppm con tres decimales'''

        return self.humo_ppm

    def get_alarma(self):
        '''Devuelve un String de la variable alarma'''

        global alarma_mq2

        return str(alarma_mq2)

    def get_voltaje(self):
        '''Devuelve un String de la variable voltaje'''

        return str(self.voltaje)

    def get_funcionamiento(self):
        '''Nos dice mediante un boolean si el sensor funciona. En el caso de True
        es que el sensor funciona'''

        return self.funcionamiento

    # cuando el sensor detecte una concentración peligrosa lanzará una alarma
    DOutput.when_pressed = activar_alarma
