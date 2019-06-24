import Adafruit_GPIO.SPI as SPI
import RPi.GPIO as GPIO
import MAX6675.MAX6675 as MAX6675
import time

FREQUENCY =  1 #Hz
SPI_PORT   = 0
SPI_DEVICE = 0
RELAY_PIN = 2

LOG = "test.csv"

def write_log(log) :
    log_file = open(LOG,'a+')
    s = ""
    for l in log :
        s += "%s,%s\n"%l

    log_file.write(s)
    log_file.close()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)
sensor = MAX6675.MAX6675(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
log = []
ltime = 0
log_cnt = 0

# try :
while True :
    temp = sensor.readTempC()
    print "TEMP: %s"%temp
    log.append((ltime,temp))
    log_cnt += 1

    time.sleep(1/FREQUENCY)
    ltime += (1/FREQUENCY)

    if log_cnt > 10 :
        log_cnt = 0
        write_log(log)
# except :
#     GPIO.output(RELAY_PIN, GPIO.HIGH)

    