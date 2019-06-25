import Adafruit_GPIO.SPI as SPI
import MAX6675.MAX6675 as MAX6675


SPI_PORT   = 0
SPI_DEVICE = 0

sensor = MAX6675.MAX6675(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

temp = sensor.readTempC()
print "TEMP: %sC"%temp