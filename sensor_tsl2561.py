# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TSL2561
# This code is designed to work with the TSL2561_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Light?sku=TSL2561_I2CS#tabs-0-product_tabset-2

import smbus
import time


class Tsl2561:
    '''Lee todos los datos del sensor Tsl2561'''

    def __init__(self):
        # Get I2C bus
        bus = smbus.SMBus(1)

        # TSL2561 address, 0x39(57)
        # Select control register, 0x00(00) with command register, 0x80(128)
        #       0x03(03)    Power ON mode
        bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
        # TSL2561 address, 0x39(57)
        # Select timing register, 0x01(01) with command register, 0x80(128)
        #       0x02(02)    Nominal integration time = 402ms
        bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)

        time.sleep(0.5)

        # Read data back from 0x0C(12) with command register, 0x80(128), 2 bytes
        # ch0 LSB, ch0 MSB
        data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)

        # Read data back from 0x0E(14) with command register, 0x80(128), 2 bytes
        # ch1 LSB, ch1 MSB
        data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)

        # Convert the data
        self.luz_total = data[1] * 256 + data[0]
        self.luz_infrarroja = data1[1] * 256 + data1[0]

    def get_luz_total(self):
        '''Devuelve la luz total en Lux sin decimales. Es necesario crear un constructor
         Tsl2561() para actualizar los datos'''

        return str("{:.0f}".format(self.luz_total))

    def get_luz_infrarroja(self):
        '''Devuelve la luz infrarroja en Lux sin decimales. Es necesario crear un constructor
         Tsl2561() para actualizar los datos'''

        return str("{:.0f}".format(self.luz_infrarroja))

    def get_luz_visible(self):
        '''Devuelve la luz visible en Lux sin decimales. Es necesario crear un constructor
         Tsl2561() para actualizar los datos'''

        return str("{:.0f}".format(self.luz_total - self.luz_infrarroja))
