import math
import logging


class Calculos:
    '''Tiene los métodos necesarios para calculas las
    PPM de cualquier sensor MQ'''

    @classmethod
    def calcular_voltaje(cls, voltaje_acumulado, cantidad_muestras):
        ''' Calcula el voltaje de media leido en un intervalo de tiempo'''

        voltaje = voltaje_acumulado / cantidad_muestras

        # en el caso de que el sensor no funcione te ponemos un valor
        # artificial en el voltaje para que el programa pueda seguir
        # funcionando.
        if(voltaje <= 0):
            voltaje = 0.001
            logging.error('Sensor de gas inutilizado')

        return voltaje

    @classmethod
    def calcular_resistencia(cls, voltaje, resistencia):
        '''Con el voltaje y la resistencia del PCB del sensor podemos calcular
        la resistentencia que te tendrá el sensor. Esta resistencia se
        representa como Rs.'''

        return float(resistencia * (4.9 - float(voltaje)) / float(voltaje))

    def calcular_ppm(self, ratio, curva_gas):
        '''Mediante calculos logaritmicos nos devuelve los ppm de un gas
        en particular.'''

        concentracion = math.pow(
            10,
            ((math.log(ratio) - curva_gas[1]) / curva_gas[2]) + curva_gas[0]
        )
        return str(round(concentracion, 3))
