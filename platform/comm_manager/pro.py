from kafka import KafkaConsumer, KafkaProducer
import json
import threading
from _thread import *
import time

import comm_module as cm


msg={"msg":"msg from app mgr"}

cm.send_message("AS",msg)

# cm.send_message_normal("AS",msg)
# producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

# def send_message(topic,msg):
# 		producer.send(topic, msg.encode('utf-8'))
# 		producer.flush()
# 		producer.close()

# msg="kafka"

# send_message('AS',msg)