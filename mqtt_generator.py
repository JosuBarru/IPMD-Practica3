import paho.mqtt.client as mqtt
import json
import time


mqtt_broker_address = "mosquitto"
mqtt_topic = "My_Topic"


def send_events(file_path, topic, time_interval=5):
    with open(file_path, 'r') as file:
        data = json.load(file)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    client.connect(mqtt_broker_address)

    for event in data:
        payload = json.dumps(event)  # Convertir el diccionario a JSON
        client.publish(topic, payload) #Enviamos mensajes al broker

    client.disconnect()

send_events("Flights.json",mqtt_topic)
