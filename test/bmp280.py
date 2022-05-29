import board
import adafruit_bmp280
i2c = board.I2C()
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

print('Temperature: {} degrees C'.format(sensor.temperature))
print('Pressure: {}hPa'.format(sensor.pressure))
