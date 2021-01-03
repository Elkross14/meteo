from gpiozero import Button

puerto_sensor = Button(5)
TAMANO_CUBETA = 0.2794
contador = 0


def cubeta_pulso():
    '''muestra la cantidad total de lluvia recogida'''
    global contador
    contador = contador + 1
    print(contador * TAMANO_CUBETA)


# ejecuta la cunfión cada vez que detecta un pulso
puerto_sensor.when_pressed = cubeta_pulso
