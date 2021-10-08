from kafka import KafkaConsumer, KafkaProducer
import json
import threading
from _thread import *
import time

def consume_msg(topic,handler_fun):

	consumer = KafkaConsumer(topic,bootstrap_servers='localhost:9092',value_deserializer=lambda m: json.loads(m.decode('utf-8')))
  
	for mess in consumer:
		th = threading.Thread(target=handler_fun,args=(mess.value,))
		th.start()


def handler_fun(msg):
	print(msg)
	# print("Handle your incomming msg dict here")
	# print(msg)

def to_recv():
	# "AS" is topic agreed between two module

	consume_msg('AS',handler_fun)
	# cm.ApplicationManager_to_Scheduler_interface(inputq)
start_new_thread(to_recv,())
# time.sleep(10)

