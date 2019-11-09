#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import telepot
import geocoder
import lcddriver
import MySQLdb
import picamera 
import paho.mqtt.client as mqtt
from telepot.loop import MessageLoop
from time import sleep
from datetime import datetime

#Start telegram 
start_tele = '''
Hi! Anh Tu Nguyen.
Command list:
/hola to say Hi. 
/time to get current time in server.
/date to get date in server. 
/getip to get current ip of server.
/location to get current location of server. 
/temp to get current temparature in house. 
/co2tvoc to get current CO2 concentration and TVOC in house.
/sendphoto to send photo from house.
/sendvideo to send video from house.
/detectormove to check move in house.
/soilmoisture to check moisture in soil.
/bye to say bye.
'''

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = lcddriver.lcd()

# Connection to MYSQL DB
db = MySQLdb.connect("localhost", "anhtu91", "nguyenanhtu59", "houseinfo")
curs = db.cursor()

# Datetime 
now = datetime.now()

#CCS811 CO2 sensor
co2 = ""
tvoc = ""
temp_ccs811 = ""
temp_dht11 = ""
humidity = ""
soil_moisture = ""
detect_move = ""

def on_connect(client, userdata, flags, rc):
    print("Connected to broker...")
    client.subscribe("co2") 
    client.subscribe("tvoc")
    client.subscribe("temp_ccs881")
    client.subscribe("temparature")
    client.subscribe("humidity")
    client.subscribe("soilmoisture")
    client.subscribe("move")
    
def on_message(client, userdata, message):
    if(message.topic == "co2"):
        global co2
        co2 = str(message.payload.decode("utf-8"))
        if(int(float(co2)) < 1000):
            co2 = str(int(float(co2))) + " "
        else:
            co2 = str(int(float(co2)))
    elif(message.topic == "tvoc"):
        global tvoc
        tvoc = str(message.payload.decode("utf-8"))
        tvoc = str(int(float(tvoc)))
    elif(message.topic == "temp_ccs881"):
        global temp_ccs811
        temp_ccs811 = str(message.payload.decode("utf-8"))
        temp_ccs811 = str(int(float(temp_ccs811)))
    elif(message.topic == "temparature"):
        global temp_dht11
        temp_dht11 = str(message.payload.decode("utf-8"))
        temp_dht11 = str(int(float(temp_dht11)))
    elif(message.topic == "humidity"):
        global humidity
        humidity = str(message.payload.decode("utf-8"))
        humidity = str(int(float(humidity)))
    elif(message.topic == "soilmoisture"):
        global soil_moisture
        soil_moisture = str(message.payload.decode("utf-8"))
        soil_moisture = str(int(float(soil_moisture)))
    elif(message.topic == "move"):
        global detect_move
        detect_move = str(message.payload.decode("utf-8"))
        detect_move = str(int(float(detect_move)))
        
#CCS811 sensor and MQTT Brocker
client = mqtt.Client()
client.username_pw_set("admin1", password='admin1')
client.connect("192.168.1.2", 1883)

client.on_connect = on_connect       #attach function to callback
client.on_message = on_message       #attach function to callback

# For Telegram message
def handle(msg):
    # Receiving the message from telegram
    chat_id = msg['chat']['id'] 
    # Getting text from the message
    command = msg['text']   

    print ('Received:')
    now = datetime.now()
    print("\tTime: "+now.strftime("%H:%M:%S %d/%m/%Y") + "\n\tCommand: "+command)
    
    command = command.lower()
    date_time = "Time " + now.strftime("%H:%M:%S %d/%m/%Y") + "\n"
    
    g = geocoder.ip('me')
    location = "Location: " + ' '.join(str(f) for f in g.latlng) + " City: "+g.city +"\n"
     
    # Comparing the incoming message to send a reply according to it
    if '/hola' in command:
        bot.sendMessage (chat_id, start_tele)
    
    elif command == '/bye':
        bot.sendMessage (chat_id, str("See you later. Anh Tu Nguyen."))
    
    elif command == '/time':
        bot.sendMessage(chat_id, str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
    
    elif command == '/date':
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    
    elif command == '/temp':
        result = ""
        if humidity is not None and temp_dht11 is not None:
            result = ("Temp = {0}°C Humidity = {1}%\n").format(temp_dht11, humidity)
        else:
            result = "Error to read data from DHT11 :(\n"
        
        bot.sendMessage(chat_id, str(date_time+location+result))
        
    elif command == '/co2tvoc':
        bot.sendMessage(chat_id, ("CO2 = {0} ppm, TVOC = {1}").format(co2,tvoc))
        
    elif command == '/location':
        bot.sendMessage(chat_id, str(location))
    
    elif command == '/getip':
        bot.sendMessage(chat_id, str(g.ip))
    
    elif command == '/sendphoto':
        #Get the photo
        camera=picamera.PiCamera()
        camera.capture('/home/pi/Pictures/capture.jpg')
        camera.close()
        # Sends a message to the chat
        bot.sendPhoto(chat_id=chat_id, photo=open('/home/pi/Pictures/capture.jpg', 'rb'))
    
    elif command == '/sendvideo':
        camera = picamera.PiCamera()
        camera.start_preview()
        camera.start_recording('/home/pi/Videos/video.h264')
        sleep(10)
        camera.stop_recording()
        camera.stop_preview()
        camera.close()
        bot.sendVideo(chat_id=chat_id, video=open('/home/pi/Videos/video.h264', 'rb'))
        
    elif command == '/detectormove':
        if(detect_move=='1'):
            bot.sendMessage(chat_id, str("Detected movement."))
        elif(detect_move=='0'):
            bot.sendMessage(chat_id, str("No movement."))
    
    elif command == '/soilmoisture':
        bot.sendMessage(chat_id, soil_moisture+"%.")
        
    else:
        bot.sendMessage(chat_id, str("Not correct command."))
           
# Insert your telegram token below
bot = telepot.Bot('XXXXXXXXXXXX') #telegram token
print (bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print ('Listening....')

# For LCD 
try:
    temporary_temp = 0
    temporary_humi = 0
    
    while True:
        client.loop_start()           
            
        #LCD display
        display.lcd_display_string(str(datetime.now().strftime("%d-%m-%Y %H:%M")), 1)
        display.lcd_display_string(temp_dht11+ "oC "+humidity+ "% " + co2+ "ppm|" , 2)
        
        client.loop_stop()
        
        '''
        if(temporary_temp != temparatur + 3) and #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        temporary_temp = temparatur
        temporary_humi = humidity
        '''
        
except KeyboardInterrupt:
    print("Clear up!")
    display.lcd_clear()

