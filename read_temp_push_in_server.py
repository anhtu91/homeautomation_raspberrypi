#!/usr/bin/python
import web
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from datetime import datetime

urls = ('/', 'index')

chon_cam_bien = Adafruit_DHT.DHT11

GPIO.setmode(GPIO.BCM)

pin_sensor = 24

class index:
    def GET(self):
        return_value = ""
        now = datetime.now()
        do_am, nhiet_do = Adafruit_DHT.read_retry(chon_cam_bien, pin_sensor)

        if do_am is not None and nhiet_do is not None:
            date_time = "Time " + now.strftime("%d/%m/%Y, %H:%M:%S") + "\n"
            #print(datetime.datetime.now())
            temp = "Temp: = {0:0.1f}  Humidity = {1:0.1f}\n".format(nhiet_do, do_am)
            #print ("Nhiet Do = {0:0.1f}  Do Am = {1:0.1f}\n").format(nhiet_do, do_am)
            return_value = date_time + temp
        else:
            #print("Loi khong the doc tu cam bien DHT11 :(\n")
            return_value = "Error. Sensor is not readable.\n"
        return return_value

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

