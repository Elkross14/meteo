from datetime import datetime
import math

from gpiozero import Button
from apscheduler.schedulers.background import BackgroundScheduler

puerto_sensor = Button(5)
contador_viento = 0
contador_viento_rafaga = 0
contador_num_rafagas = 0
vel_max_racha = 0
vel_med = 0


class VelocidadViento:

    def __init__(self):

        # Mide las rafagas de viento cada 20 segundos
        sched = BackgroundScheduler()
        sched.add_job(self.medirRafaga, 'interval', seconds=20)
        sched.start()

    def pulso(self):

        global contador_viento
        global contador_viento_rafaga

        contador_viento = contador_viento + 1
        contador_viento_rafaga = contador_viento_rafaga + 1

    def medirRafaga(self):

        global contador_viento_rafaga
        global contador_num_rafagas
        global vel_max_racha

        vel_rafaga = self.calcularVelocidad(contador_viento_rafaga, 20)

        if vel_rafaga > vel_max_racha:
            vel_max_racha = vel_rafaga

        contador_viento_rafaga = 0
        contador_num_rafagas = contador_num_rafagas + 1

    def calcularVelocidad(self, contador, intervalo):

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

        print("velocidad = " + str(velocidad_real) + "km/h")

        return velocidad_real

    def calcularVelocidadMedia(self):
        global contador_viento
        global contador_num_rafagas
        global vel_med

        # para saber cuanto tiempo lleva el programa recogiendo datos miramos
        # los ciclos de rachas hecho y los multiplicamos por 20 para obtener
        # los segundos.
        tiempo = contador_num_rafagas * 20

        # Calculamos la velocidad del viento promedio en km/h
        vel_med = self.calcularVelocidad(contador_viento, tiempo)

        # reiniciamos el contador para la siguiente hora
        contador_viento = 0
        contador_num_rafagas = 0

    def getVelMedia(self):
        return str("{:.3f}".format(vel_med))

    def getVelMaxRacha(self):
        return str("{:.3f}".format(vel_max_racha))

    puerto_sensor.when_pressed = pulso
