from uuid import uuid1
from paho.mqtt.subscribeoptions import SubscribeOptions
import paho.mqtt.client as mqtt

from messageFactory import generateCapabilityStructureMessage, generateRegisterMessage


def registerFin(mqttc: mqtt.Client, fin_id: str, ack_awaiter):
    # noLocal:            True or False. If set to True, the subscriber will not receive its own publications.
    # Does not seem to work
    mqttc.subscribe(
        "soarca", options=SubscribeOptions(qos=1, noLocal=True))

    x = generateCapabilityStructureMessage(str(uuid1()), "cap1", "", "")
    msg = generateRegisterMessage(fin_id)
    msg.capabiltities.append(x)
    json_msg = msg.toJson()
    mqttc.subscribe(
        fin_id, options=SubscribeOptions(qos=1, noLocal=True))

    ack_awaiter(msg.message_id, lambda:
                mqttc.publish("soarca", json_msg, qos=1))
