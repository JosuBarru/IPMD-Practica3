from time import sleep
from kafka import KafkaProducer
import json
import yaml

with open("./config.yml", 'r') as ymlfile:
    topic_list = yaml.load(ymlfile, Loader=yaml.FullLoader)

CODE = 'PRODUCER'
BROKER = topic_list[CODE]['BROKER']
PRODUCER_TOPIC = topic_list[CODE]['TOPIC']

# Configurar el productor de Kafka
producer = KafkaProducer(bootstrap_servers=BROKER)

# Leer el archivo JSON y enviar eventos a Kafka
def send_events(file_path, topic, time_interval=5):
    with open(file_path, 'r') as file:
        data = json.load(file)
        for event in data:
            producer.send(topic, json.dumps(event).encode('utf-8'))
            sleep(time_interval)

# Llamar a la función para enviar eventos
send_events("Flights.json", PRODUCER_TOPIC)


