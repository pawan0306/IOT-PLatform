from kafka import KafkaConsumer, KafkaProducer
import json
    
def send_message(topic,mess):
  producer = KafkaProducer(bootstrap_servers='localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))  
  producer.send(topic, mess)
  producer.flush()
  producer.close()


mess={"msg":"my msg"}

send_message("AS",mess)