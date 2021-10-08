import _thread
import requests
import json
from kafka import KafkaConsumer
import ServerLifeCycleManager as sl
import threading
import os
import sys

sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
import comm_module as cm

jobID = {}


def createConfig(sensorList, path):
    with open(path+'/conf.json', 'w') as f:
        data = {}
        for i in sensorList:
            i = i.split('_')
            data[i[0]] = i[1]
        f.write(json.dumps(data))


def appExe(action, jID, algoID, appID, userID, devID, RAM, CPU, path):
    global jobID
    ip, port = sl.running_runtime()
    if action == 'start':
        #ip ="127.0.0.1"
        #port = "5010"
        """
        consumer = KafkaConsumer('node-server-assign',bootstrap_servers=['localhost:9092'],auto_offset_reset='latest',enable_auto_commit=True,value_deserializer=lambda x: json.loads(x.decode('utf-8')))
        for message in consumer:
            ip = message.value["host"]
            port = message.value["port"]
            break
        """
        print("IP/port assign to job {} is {}/{}".format(jID, ip, port))
        jobID[jID] = [ip, port]
        status = requests.get("http://"+ip+':'+port+'/runapp', params={'app_id': appID, 'user_id': userID, 'ram_req': RAM,
                                                                       'cpu_req': CPU, 'algo_path': path+"/"+devID+"/"+appID, 'app_path': path+"/"+devID+"/"+appID+"/"+algoID+"/main.py"})
        if status:
            print("Application:{} Started".format(appID))

    else:
        status = requests.get("http://"+jobID[jID][0]+':'+jobID[jID]
                              [1]+'/stopapp', params={'app_id': appID, 'user_id': userID})
        if status:
            del jobID[jID]
            print("Application:{} terminated".format(appID))


def handler_fun(message):
    action = message["action"]  # start/stop
    jID = message["jID"]
    appID = message["appID"]
    algoID = message["algoID"]
    sensorList = message["sensorList"]  # ["temp_t123","ac_a123"]
    userID = message["userID"]
    devID = message["devID"]
    RAM = message["RAM"]
    CPU = message["CPU"]
    #path = os.path.abspath()
    #path = "/".join(path) + '/AppManager/Applications'
    path = '../Applications'
    createConfig(sensorList, path + "/"+devID+"/"+appID+"/"+algoID)
    appExe(action, jID, algoID, appID, userID, devID, RAM, CPU, path)


def main():
    while(1):
        # schObj=Scheduler(dataDc=None)
        t2 = threading.Thread(target=cm.consume_msg("DP", handler_fun))
        t2.start()

    # appExe()
    # cm.consume_msg('DP',handler_fun)


main()
