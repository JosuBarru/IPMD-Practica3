import paho.mqtt.client as mqtt
import json
import yaml

with open("./config.yml", 'r') as ymlfile:
    topic_list = yaml.load(ymlfile, Loader=yaml.FullLoader)

CODE = 'GENERADOR'
BROKER = topic_list[CODE]['BROKER']
GENERATOR_TOPIC = topic_list[CODE]['TOPIC']



def send_events(file_path, topic, time_interval=5):
    print(BROKER)
    print(GENERATOR_TOPIC)
    with open(file_path, 'r') as file:
        data = json.load(file)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.connect(BROKER)

    for event in data:
        payload = json.dumps(event)  #Convertimos el diccionario a JSON
        client.publish(topic, payload) #Enviamos mensajes al broker

    client.disconnect()

send_events("Flights.json",GENERATOR_TOPIC)
