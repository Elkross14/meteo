import math
from gpiozero import Button
from apscheduler.schedulers.background import BackgroundScheduler

PUERTO_SENSOR = Button(6)

contador_viento = 0
contador_viento_rafaga = 0


class VelocidadViento:
    '''Lee la velocidad del viento en racha y promedio en Km/h. No retorna decimales'''

    vel_med = 0
    vel_max_racha_comparar = 0
    vel_max_racha = 0
    contador_num_rafagas = 0

    def __init__(self):
        '''Inicia un scheduler para recoger las ráfagas de viento cada 5 segundos.'''

        # Mide las rafagas de viento cada 5 segundos
        sched = BackgroundScheduler()
        sched.add_job(self.medir_rafaga, 'interval', seconds=5)
        sched.start()

    def pulso(self):
        '''Suma 1 a los contadores de viento y viento_rafaga cada vez que se ejecuta'''

        global contador_viento
        global contador_viento_rafaga

        contador_viento += 1
        contador_viento_rafaga += 1

    def medir_rafaga(self):
        '''medirá la velocidad de la ráfaga de viento y lo comparará con la velocidad
        máxima registrada en racha y la cambiará si la actual es superior.'''

        global contador_viento_rafaga

        vel_rafaga = self.calcular_velocidad(contador_viento_rafaga, 5)

        if vel_rafaga > self.__class__.vel_max_racha_comparar:
            self.__class__.vel_max_racha_comparar = vel_rafaga

        contador_viento_rafaga = 0
        self.__class__.contador_num_rafagas += 1

    def calcular_velocidad(self, contador, intervalo):
        '''Calcula la velocidad del viento ya sea media o de racha.'''

        # Calcular la circunferencia del sensor de viento
        circunferencia_cm = (2 * math.pi) * 9.0

        # Dividimos los pulsos recibidos entre 2 ya que lanza dos pulsos por vuelta
        rotaciones = contador / 2

        # Calculamos la distancia en km
        dist_km = (circunferencia_cm * rotaciones) / 100000

        # calculamos la velocidad en Km/h
        velocidad = (dist_km / intervalo) * 3600

        # multiplicamos la velocidad por 1.18 que es la fuerza del viento perdida
        # por el rozamiento del sensor de viento
        velocidad_real = velocidad * 1.18

        return velocidad_real

    def finalizar_ciclo(self):
        '''llama a los métodos necesarios para finalizar el ciclo de lectura y 
        empezar uno nuevo'''

        self.calcular_velocidad_media()
        self.reiniciar_valores()

    def calcular_velocidad_media(self):
        '''Calcula la velocidad media registrada.'''

        # para saber cuanto tiempo lleva el programa recogiendo datos miramos
        # los ciclos de rachas hecho y los multiplicamos por 5 para obtener
        # los segundos.
        tiempo = self.__class__.contador_num_rafagas * 5

        # Evitamos que mida entre cero en el caso de que ejecute el comando antes de 5
        # segundos de haber iniciado el programa.
        if tiempo != 0:

            # Calculamos la velocidad del viento promedio en km/h
            self.__class__.vel_med = self.calcular_velocidad(
                contador_viento, tiempo)

        else:
            self.__class__.vel_med = 0

    def reiniciar_valores(self):
        '''Reiniciamos los valores de las variables para empezar de nuevo el siguiente
        ciclo.'''

        global contador_viento

        contador_viento = 0
        self.__class__.contador_num_rafagas = 0
        self.__class__.vel_max_racha = self.__class__.vel_max_racha_comparar
        self.__class__.vel_max_racha_comparar = 0

    def get_vel_media(self):
        '''Devuelve la velocidad media del viento sin decimales.'''

        return str(round(self.__class__.vel_med))

    def get_vel_max_racha(self):
        '''Devuelve la racha de viendo con mayor velocidad en el intervalo del
        tiempo sin decimales'''

        return str(round(self.__class__.vel_max_racha))

    # Envía un pulso cada vez que el anemómetro da media vuelta.
    PUERTO_SENSOR.when_pressed = pulso
