
from kafka import KafkaConsumer, KafkaProducer
import json
import threading
from _thread import *
import time


def send_message(topic, mess):
    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(topic, mess)
    producer.flush()
    producer.close()

# def send_message_normal(topic,mess):
#   producer = KafkaProducer(bootstrap_servers='localhost:9092')
#   producer.send(topic, mess)
#   producer.flush()
#   producer.close()


def consume_msg(topic, handler_fun):
    consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092',
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for mess in consumer:
        th = threading.Thread(target=handler_fun, args=(mess.value,))
        th.start()


def consume_msg_once(topic, handler_fun):
    consumer = KafkaConsumer(topic, bootstrap_servers='localhost:9092',
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    for mess in consumer:
        th = threading.Thread(target=handler_fun, args=(mess.value,))
        th.start()
        break


def consume_msg_all(topic, handler_fun):  # not working
    # consumer = KafkaConsumer(topic,bootstrap_servers='localhost:9092'
    # 	,value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    # 	# ,auto_offset_reset='earliest'
    # 	# ,group_id=None
    # 	)
    consumer = KafkaConsumer(topic,
                             bootstrap_servers=['localhost:9092'],
                             value_deserializer=lambda m: json.loads(
                                 m.decode('utf-8')),
                             # group_id=None,
                             # auto_commit_enable=False,
                             auto_offset_reset='earliest')
    for mess in consumer:
        th = threading.Thread(target=handler_fun, args=(mess.value,))
        th.start()
