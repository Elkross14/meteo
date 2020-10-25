from gpiozero import Button

PUERTO_SENSOR = Button(6)
TAMANO_CUBETA = 0.2794
contador = 0


class Pluviometro:
    '''Lee la cantidad de lluvia en un intervalo de tiempo'''

    def __init__(self):

        self.litros = 0

    def cubeta_pulso(self):
        '''Suma 1 cada vez que la cubeta del pluviometro se vacia.'''

        global contador

        contador += 1

    def calcular_lluvia(self):
        '''Devuelve la cantidad de lluvia en litros con un decimal'''

        global contador

        self.__class__.litros = contador * TAMANO_CUBETA

    def get_litros(self):
        '''Devuelve los litros de agua acumulados en un metro cúbico
        con un solo decimal.'''

        return str("{:.1f}".format(self.__class__.litros))

    def reiniciar_valores(self):
        '''Reiniciamos los valores de las variables para empezar de nuevo el siguiente
        ciclo.'''

        global contador

        contador = 0

    # Envía un pulso cada vez que la cubeta se vacia
    PUERTO_SENSOR.when_pressed = cubeta_pulso
