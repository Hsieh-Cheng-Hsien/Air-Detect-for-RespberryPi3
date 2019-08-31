# -*- coding: utf-8 -*-
import sys, time, urllib2
from Adafruit_CCS811 import Adafruit_CCS811
from Adafruit_BME280 import BME280_OSAMPLE_8
from Adafruit_BME280 import BME280
import SDL_Pi_HDC1000
import datetime
from picamera import PiCamera
from subprocess import Popen, PIPE
import threading
from time import sleep
import os, fcntl
import cv2
from shutil import copyfile

#spawn darknet process
yolo_proc = Popen(["./darknet",
                    "detect",
                    "./cfg/yolov3-tiny.cfg",
                   "./yolov3-tiny.weights",
                   "-thresh","0.1"],
                   stdin = PIPE, stdout = PIPE)
fcntl.fcntl(yolo_proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

def thingSpeak(CO2, TVOC, Temperature, Humidity, AtmosphericPressure, Human):
    print 'Sending to ThingSpeak API...'
    url = "https://api.thingspeak.com/update?api_key="
    url += THINGSPEAK
    url += "&field1="
    url += str(CO2)
    url += "&field2="
    url += str(TVOC)
    url += "&field3="
    url += str(Temperature)
    url += "&field4="
    url += str(Humidity)
    url += "&field5="
    url += str(AtmosphericPressure)
    url += "&field6="
    url += str(Human)
    #print url
    try: 
      content = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
      print "Invalid HTTP response"
      return False
    print 'Done'
    #print content
    
ccs =  Adafruit_CCS811()
sensor = BME280(
    t_mode=BME280_OSAMPLE_8,
    p_mode=BME280_OSAMPLE_8,
    h_mode=BME280_OSAMPLE_8,
    address=0x76
    )
def ccs811example():
    """Get the data from the CCS811 sensor module and return it"""
    
    #if ccs.available():
        #temp = ccs.calculateTemperature()
    #co2 = ccs.geteCO2()
    #voc = ccs.getTVOC()
    if not ccs.readData():
        co2 = ccs.geteCO2()
        tvoc = ccs.getTVOC()
    else:
       print "ERROR!"
            
    #Print Data information on screen
    print('CO2:{0} ppm, TVOC:{1} ppm'.format(co2, tvoc))
    return co2,tvoc
    
def bme280example():
    """The address parameter is important here as most BME/P280 sensors occupy the default 0x77 address as noticed in the Adafruit library.
       This can be easily verified by running i2cdetect -y 1 on your Pi"""
    temp = sensor.read_temperature()
    pascals = sensor.read_pressure()
    pres = pascals / 100
    humd = sensor.read_humidity()
    #Print Data information on screen
    print('Temperature:{0} degC, Pressure:{1} hPa, Humidity:{2} %'.format(temp, pres, humd))
    return temp,pres,humd
    
def hdc1080examples():
    hdc1000 = SDL_Pi_HDC1000.SDL_Pi_HDC1000()
    temp = hdc1000.readTemperature()
    humd = hdc1000.readHumidity()
    #Print Data information on screen
    print('Temperature:{0} degC, Humidity:{1} % '.format(temp, humd))
    return temp,humd

if __name__ == '__main__':   
    THINGSPEAK = '357YZP46SGG344K5'
    try:
        while(1):
            t = time.strftime("%Y-%m-%d %H:%M:%S")
            print "Program Started at:" + t
            personCount = 0

            def picamera():
                global personCount
                try:
                    camera = PiCamera()
                    camera.resolution = (2592, 1700)
                    camera.rotation=180                        
                    stdout = yolo_proc.stdout.read()
                    if 'Enter Image Path' in stdout:
                        #camera.rotation=180
                        camera.capture('frame.jpg')
                        yolo_proc.stdin.write('frame.jpg\n')
                        
                    if len(stdout.strip())>0:
                        #print('get %s' % stdout)
                        #print()
                        if 'person' in stdout:
                            personCount = stdout.count('person')  
                        else:
                            personCount = 0
                    print("personCount:", personCount)                      
                    
                except Exception as e:
                    errorTime = datetime.datetime.now()
                    errorFile = open("errorFile.txt", "a")
                    errorFile.write("Loop1: {0}, {1}\n".format(errorTime, str(e)))
                    pass
            
            #Create a subthread
            t1 = threading.Thread(target = picamera)
            #Start the execution
            t1.start()
            #AirSensor
            ccs811 = ccs811example()
            bme280 = bme280example()
            hdc1080 = hdc1080examples()
            Time = datetime.datetime.now()
            t1.join()
                 
            #Including time, Co2, tvoc, temp, humd, pressure.
            data = (str(t), "\n", str(ccs811[0]), ",", str(ccs811[1]), ",", str((bme280[0]+hdc1080[0])/2), ",", str(hdc1080[1]), ",", str(bme280[1]), ",", str(personCount),"\n")
            f = open("AirProject_log.txt", "a")
            f.write("".join(data))
            f.close()
            print(data)
            print "--------------------------------------------------------------"
            try:
                if(THINGSPEAK is not False):
                    thingSpeak(ccs811[0], ccs811[1], (bme280[0]+hdc1080[0])/2, hdc1080[1], bme280[1], personCount)
            except Exception:
                pass
            #Capture Time, on the minute
            now = datetime.datetime.now()
            now_sec = now.second
            sec_to_zero = 59 - now_sec
            tim.sleep(now_sec)
    except Exception as e:
        errorTime = datetime.datetime.now()
        errorFile = open("errorFile.txt", "a")
        errorFile.write("Loop2: {0}, {1}\n".format(errorTime, str(e)))
        pass
        os.system('sudo reboot now')
