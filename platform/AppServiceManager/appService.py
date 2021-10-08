#!/usr/bin/env python3

import _thread
import requests
import json
from kafka import KafkaConsumer
import ServerLifeCycleManager as sl
import threading
import os
import sys 
import pandas as pd
import shutil

sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
import comm_module as cm

jobID = {}

def createList(idby, types):

    if idby[0] == 'location':
        index = 'loc'
    else:
        index = 'desc'
    df = pd.read_csv('../SensorManager/running_sensors.txt', delimiter = ",")
    sensorList = {}
    for i in types:
        sensorList[i] = list(df[(df[index] == idby[1]) & (df['type'] == i)]['topic'])

    return sensorList


def createConfig(conf, path):
    print(path)
    with open(path+'/conf.json', 'w') as f:
        data = {}
        """for i in sensorList:
            i = i.split('_')
            data[i[0]] = i[1]"""
        f.write(json.dumps(conf))


def appExe(jID, algoID, appID, userID, devID, RAM, CPU, dirpath):
    
    global jobID
    ip, port = sl.running_runtime()

    print(f'-------Job ID assigned: {jID}')
    print(f"-------Server assigned with IP/port: {ip}{port}")
    
    jobID[jID] = [ip, port]
    status = requests.get("http://"+ip+':'+str(port)+'/runapp', params={'jID':jID, 'app_path':dirpath+"/"+algoID+".py"})
    if status:
        print("-------Application:{} Started".format(appID))

def appStop(jID):

    global jobID

    status = requests.get("http://"+jobID[jID][0]+':'+str(jobID[jID][1])+'/stopapp', params={'jID':jID})
    if status:
        shutil.rmtree('../RunningApps/'+jID)
        del jobID[jID]
        print("-------Application:{} terminated".format(jID.split('_')[-1]))


def handler_fun(message):

    if message['action'] == 'start':
        action = message["action"]  # start/stop
        jID = message["jID"]
        appID = message["appID"]
        algoID = message["algoID"]
        types = message['sensorList'] #[type1,type2...]
        userID = message["userID"]
        devID = message["devID"]
        RAM = message["RAM"]
        CPU = message["CPU"]
        location = message["location"]
        placeholder = message["placeholder"]
        path = '../RunningApps/'

        if placeholder != '':
            idby = ['placeholder', placeholder]
        else:
            idby = ['location', location]


        print(f"Request recived to RUN {algoID}")

        sensorList = createList(idby, types)
        if message['placeholder'] != '':
            outputfile = message['placeholder']+'_'+userID+'_'+appID+'_'+algoID
        else:
            outputfile = message['location']+'_'+userID+'_'+appID+'_'+algoID

        conf = {'sensors':sensorList,'userID':userID,'outputfile':'../Data/'+outputfile}
        dirpath = path+outputfile
        
        with open('../Data/'+outputfile, 'a') as f:
            pass
        
        try:
            os.mkdir(dirpath)
        except Exception:
            pass

        createConfig(conf, dirpath)

        print(f'-------config file generated')

        appExe(jID, algoID, appID, userID, devID, RAM, CPU, dirpath)
    
    else:
        jID = message['jID']
        print(f'Request recived to STOP APP with Job ID: {jID}')
        appStop(message['jID'])


def schedular_service():
    consumer = KafkaConsumer('DP', bootstrap_servers='localhost:9092',
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for mess in consumer:        
        _thread.start_new_thread(handler_fun,(mess.value,))


def run_triggeredApp(path, jID):
    global jobID

    ip, port = sl.running_runtime()
    
    print(f"Request recieved to RUN {path.split('/')[-1]}")
    print(f'-------Job ID assigned: {jID}')
    print(f"-------Server assigned with IP/port: {ip}{port}")
    
    jobID[jID] = [ip, port]
        
    status = requests.get("http://"+ip+':'+str(port)+'/trigger', params={'app_path': path})
    if status:
        appName = path.split('/')[-1]
        print(f'Application:{appName} Started')


def trigger_service():
    jID = 1
    consumer = KafkaConsumer('trig', bootstrap_servers='localhost:9092',
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for mess in consumer:
        run_triggeredApp(mess.value['path'], 'jbid'+str(jID))   
        jID += 1

def main():
        print("***************AppService Manager Started***************\n")
        t1 = threading.Thread(target=schedular_service)
        t2 = threading.Thread(target=trigger_service)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

main()
