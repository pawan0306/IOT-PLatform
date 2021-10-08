#!/usr/bin/env python3

from kafka import KafkaConsumer
from json import loads
import sys
import subprocess

from models import *
sys.path.insert(0, sys.path[0][:sys.path[0].rindex('/')] + '/comm_manager')
consumer = KafkaConsumer(KAFKA_TOPIC_SERVER_LIST, bootstrap_servers=[
                         'localhost:9092'], auto_offset_reset='earliest', enable_auto_commit=True, group_id='my-group', value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    message = message.value
    print(message)

# subprocess.run([sys.executable, 'pawan/app1.py'])
