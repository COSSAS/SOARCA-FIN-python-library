from uuid import uuid1
from paho.mqtt.subscribeoptions import SubscribeOptions
import paho.mqtt.client as mqtt

from messageFactory import generateCapabilityStructureMessage, generateRegisterMessage
from models.register import Register


def registerFin(mqttc: mqtt.Client, message: Register, ack_awaiter):
    # noLocal:            True or False. If set to True, the subscriber will not receive its own publications.
    # Does not seem to work
    mqttc.subscribe(
        "soarca", options=SubscribeOptions(qos=1, noLocal=True))

    json_msg = message.model_dump_json()
    mqttc.subscribe(
        message.fin_id, options=SubscribeOptions(qos=1, noLocal=True))

    ack_awaiter(message.message_id, lambda:
                mqttc.publish("soarca", json_msg, qos=1))
