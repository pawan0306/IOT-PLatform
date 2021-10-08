#!/usr/bin/env python3

import time
import sys
import json

# TODO: Uncomment next line
sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
import comm_module as cm
from kafka import KafkaConsumer, KafkaProducer
from simulators import *


def simulate(sensor_obj):

    topic = sensor_obj.id
    init = True
    consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092', auto_offset_reset='latest', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    while True:
        if not init:
            for message in consumer:
                msg = message.value
                break
            sensor_obj.controller = msg['controller']
            init = False
        
        data, controller = sensor_obj.genRandom()

        print(f"{sensor_obj.id} ---> Data:", data)
        print(f"{sensor_obj.id} ---> Controller:", controller)

        msg = {'data': data, 'controller': controller}

        # TODO: Uncomment next line
        producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send(topic, msg)
        time.sleep(1)
