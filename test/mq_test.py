# nativas de Python
import time

# I2C comunicación
import board
import busio

# librerías del ADC ADS1115
import adafruit_ads1x15.ads1115 as ads1115
from adafruit_ads1x15.analog_in import AnalogIn

# lectura digital
from gpiozero import Button


# direccion I2C del ADS11115
ADDRESS = 0x49# address conectado a VDD
PIN = 0# canal analógico del chip

convertor = ads1115.ADS1115

i2c = busio.I2C(board.SCL, board.SDA)
adc = convertor(i2c=i2c, address=ADDRESS)

channel = AnalogIn(adc, PIN)

while True:
    print(channel.voltage)
    time.sleep(1)
