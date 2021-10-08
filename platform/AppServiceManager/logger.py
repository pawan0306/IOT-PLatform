#!/usr/bin/env python3

from kafka import KafkaConsumer
from json import *
import sys
import subprocess

from models import *

consumer = KafkaConsumer(KAFKA_TOPIC_LOGGER, bootstrap_servers=[
    'localhost:9092'], auto_offset_reset='earliest', enable_auto_commit=True, group_id='my-group', value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    message = message.value
    print(message)
    info = load(message)
    sender = '??' if 'sender' not in info else info['sender']
    type = 0 if 'type' not in info else info['type']
    msg = '??' if 'msg' not in info else info['msg']
    if type == 3:
        type = 'NOTIF'
    elif type == 1:
        type = 'INFO'
    elif type == 2:
        type = 'ERROR'
    else:
        type = 'UNKNOWN'
    with open('../Logs/'+sender) as f:
        f.write(f'[{type}] : {sender} says {msg}\n')
    print(f'[{type}] : {sender} says {msg}')

# subprocess.run([sys.executable, 'pawan/app1.py'])
