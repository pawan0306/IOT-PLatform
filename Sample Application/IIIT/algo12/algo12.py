import API 
import math
import time
import threading

temp_threshold_max = 30
temp_threshold_min = 20
lux_threshold_max = 15
lux_threshold_min = 5

rate = 10 

count = 0

api = API.sensorapi()

iiit_loc= [30.44523, 40.54232]

def calculate_fare(gps, iiit_loc):
    return math.sqrt((float(gps[0])-iiit_loc[0])**2 + (float(gps[1])-iiit_loc[1])**2)*rate

def checkBIO():
    global count
    global gps
    while count <= 15:
    
        biometric = api.getData("BIOMETRIC")["data"][0]
        fare = calculate_fare(gps[1], iiit_loc)
        api.display(f'{time.ctime()} :: {gps[0]}:{biometric[1]} => Fare : {fare}')
        api.sendMail(f'{time.ctime()} :: {gps[0]}:{biometric[1]} => Fare : {fare}')
        count += 1

gps = api.getData("GPS")["data"][0]
t1 = threading.Thread(target=checkBIO)
t1.start()

lflag=0
tflag=0
while True:
    
    gps = api.getData("GPS")["data"][0] #{data:[[placeholderID, [x, y]]}

    if gps[1] != iiit_loc and count > 0:
        
        temp = api.getData("TEMP")["data"][0]
        lux = api.getData("LIGHT")["data"][0]

        if temp < 20 or temp > 30: 
        
            if (not tflag) and temp > 30:
                tflag = 1
                ack = api.setData(0, "TEMP",1)["data"]
                if ack == 1:
                    api.display(f'{time.ctime()} :: {gps[0]}:High temperature({temp}C) detected! AC has been Turned ON')
            if tflag and temp < 20:
                tflag = 0
                ack = api.setData(0, "TEMP",-1)["data"]
                if ack == 1:
                    api.display(f'{time.ctime()} :: {gps[0]}:Low temperature({temp}C) detected! AC has been Turned OFF')
            
        
        if lux < 5 or lux > 15: 
        
            if lflag and lux < 5:
                lflag = 0
                ack = api.setData(0, "LIGHT",1)["data"]
                if ack == 1:
                    api.display(f'{time.ctime()} :: {gps[0]}:Low intensity light({lux}) detected! Lights has been Turned ON')
            if (not lflag) and lux > 15:
                lflag = 1
                ack = api.setData(0, "LIGHT",-1)["data"]
                if ack == 1:
                    api.display(f'{time.ctime()} :: {gps[0]}:High intensity light({lux}) detected! Lights has been Turned OFF')
