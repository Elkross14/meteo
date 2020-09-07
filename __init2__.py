# datetime nos porporcionará la fecha de lectura
from datetime import datetime
import time

from sensor_dht11 import Dht11
from sensor_bmp180 import Bmp180
from sensor_tsl2561 import Tsl2561


class Main:

    fecha_y_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(fecha_y_hora)
    print("")

    # sensor dht11
    objeto_dht11 = Dht11()

    temperatura_str = objeto_dht11.getTemperature()
    humedad_str = objeto_dht11.getHumidity()

    print("DHT11" +
          "\nTemperatura: " + temperatura_str +
          "\nHumedad: " + humedad_str)
    print("")

    # sensor bmp180
    objeto_bmp180 = Bmp180()

    presion_bmp180_str = objeto_bmp180.getPresion()
    temperatura_bmp180_str = objeto_bmp180.getTemperatura()
    altura_bmp180_str = objeto_bmp180.getAltura()

    print("BMP180" +
          "\nPresión: " + presion_bmp180_str +
          "\nTemperatura: " + temperatura_bmp180_str +
          "\nAltura: " + altura_bmp180_str)
    print("")

    # sensor tsl2561
    objeto_tsl2561 = Tsl2561()

    luz_total_tsl2561_str = objeto_tsl2561.getLuzTotal()
    luz_infrarroja_tsl2561_str = objeto_tsl2561.getLuzInfrarroja()
    luz_visible_tsl2561_str = objeto_tsl2561.getLuzVisible()

    print("TSL2561" +
          "\nLuz total: " + luz_total_tsl2561_str +
          "\nLuz infrarroja: " + luz_infrarroja_tsl2561_str +
          "\nLuz visible: " + luz_visible_tsl2561_str)
    print("")
