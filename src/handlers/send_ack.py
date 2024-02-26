import paho.mqtt.client as mqtt

from messageFactory import generateAckMessage


def send_ack(mqttc: mqtt.Client, message_id: str):
    ack = generateAckMessage(message_id)

    mqttc.publish("soarca", payload=ack.toJson(), qos=1)
