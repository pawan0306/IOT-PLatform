#!/usr/bin/env python3

import bind_data
from kafka import KafkaConsumer, KafkaProducer
import threading
import json
import time
import sys
from simulators import *
import csv

# TODO: Uncomment next line
sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
import comm_module as cm


SENSOR_TYPES = {'TEMP': -1,'BIOMETRIC': -1, 'GPS': -1, 'LIGHT': -1, 'OXIMETER':-1}

sensor_objects = {}


def dummy1(topicid, handler):
    cm.consume_msg(topicid, handler)


'''
Binds the sensor data to a topic
:param sensor_info = {'type': stype, 'ip': ip, 'port': port, 'topic': topic} 

'''
def bind_sensor(sensor_info):
    global sensor_objects
    
    sensor_type = sensor_info['type']

    if sensor_type == 'TEMP':
        topic = sensor_info['topic']
        obj = TempSensor(topic, sensor_info['desc'], ip=sensor_info['ip'], loc=sensor_info['loc'], port=sensor_info['port'])
        sensor_objects[topic] = obj

    elif sensor_type == 'LIGHT':
        topic = sensor_info['topic']
        obj = LuxSensor(topic, sensor_info['desc'], ip=sensor_info['ip'], loc=sensor_info['loc'], port=sensor_info['port'])
        sensor_objects[topic] = obj

    elif sensor_type == 'BIOMETRIC':
        topic = sensor_info['topic']
        obj = BiometricSensor(topic, sensor_info['desc'], ip=sensor_info['ip'], loc=sensor_info['loc'], port=sensor_info['port'])
        sensor_objects[topic] = obj

    elif sensor_type == 'GPS':
        topic = sensor_info['topic']
        obj = GPSSensor(topic, sensor_info['desc'], ip=sensor_info['ip'], loc=sensor_info['loc'], port=sensor_info['port'])
        sensor_objects[topic] = obj

    else:
        print("ERROR: Invalid Sensor Type")
        return

    t = threading.Thread(target=bind_data.simulate, kwargs={"sensor_obj": obj})
    t.start()


def get_data(topic):
    if topic.startswith("BIOMETRIC"):
        time.sleep(10)

    consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092', group_id=None, value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for message in consumer:
        msg = message.value
        break

    print(f"SensorID: {topic} ===> Data: {msg['data']}")
    return msg['data']


def run_sensors():
    registry = open('sensor_registry.txt', 'r')

    running = open('running_sensors.txt', 'a', newline='')
    fieldnames = ['loc', 'desc', 'type', 'topic', 'ip', 'port']
    writer1 = csv.DictWriter(running, fieldnames=fieldnames)
    writer1.writeheader()
    running.close()

    global SENSOR_TYPES
    while True:

        sensors = registry.readlines()

        if len(sensors) > 0:
            for sensor in sensors:
                sensor = sensor.strip('\n')
                stype, locinfo, nwinfo = sensor.split(':')
                desc, loc = locinfo.split('_')
                ip, port = nwinfo.split('_')
                SENSOR_TYPES[stype] += 1
                topic = stype + "_" + str(SENSOR_TYPES[stype])

                sensor_info = {'type': stype, 'ip': ip, 'port': port, 'topic': topic, 'desc': desc, 'loc':loc}
                bind_sensor(sensor_info)
                print(sensor_info)
                with open('running_sensors.txt', 'a', newline='') as f:
                    # line = sinfo + ":" + nwinfo + ":" + topic
                    # print(line)
                    # f.write(line + '\n')
                    writer2 = csv.DictWriter(f, fieldnames=fieldnames)
                    writer2.writerow(sensor_info)

        time.sleep(20)

    registry.close()


def set_data(msg):
    global sensor_objects
    topic = msg['topic']
    status = msg['value']
    consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092', group_id=None, value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for message in consumer:
        msg = message.value
        break
    old_val = msg['controller']
    msg['controller'] = status
    print(f"SensorID: {topic} ===> Controller: (before){old_val} --> (after){status}")
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(topic, msg)


def start():
    #   Create a kafka topic to start sensor manager services
    t1 = threading.Thread(target=run_sensors)
    t1.start()
    print("**************** Sensor Manager ******************")
