import paho.mqtt.client as mqtt

from messageFactory import generateNackMessage


def send_nack(mqttc: mqtt.Client, message_id: str):
    nack = generateNackMessage(message_id)

    mqttc.publish("soarca", payload=nack.toJson(), qos=1)
