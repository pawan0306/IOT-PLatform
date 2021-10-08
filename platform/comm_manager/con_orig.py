from kafka import KafkaConsumer, KafkaProducer
import json
import threading
from _thread import *
import time
import comm_module as cm


def handler_fun(msg):
	# print(msg["msg"])
	# print("Handle your incomming msg dict here")
	print(msg)


def to_recv():
	# "AS" is topic agreed between two module

	# cm.consume_msg_once('AS',handler_fun)
	cm.consume_msg('AS',handler_fun)

	# cm.ApplicationManager_to_Scheduler_interface(inputq)
start_new_thread(to_recv,())
time.sleep(20)



# cm.consume_msg('AS',handler_fun)

























# def consume_message(topic):

# 	consumer = KafkaConsumer(topic,
# 		bootstrap_servers=['localhost:9092'],
#         # group_id=None,

#         # auto_offset_reset='earliest'

#                    )
# 	# print(len(consumer))
# 	for mess in consumer:
# 		print("hi")
# 		print (str(mess.value.decode('utf-8')))

# consume_message('AS')