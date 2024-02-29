import paho.mqtt.client as mqtt
import logging as log

from handlers.send_ack import send_ack
from handlers.send_nack import send_nack
from models.unregister import Unregister
from models.capabilityStructure import CapabilityStructure


def unregister_fin_handler(mqttc: mqtt.Client, message: Unregister, capabilities: list[CapabilityStructure]):
    try:
        mqttc.unsubscribe(message.fin_id)
        mqttc.unsubscribe("soarca")
        # Should we shut down the thread pool?

        log.debug("Sending unregister ack back")
        send_ack(mqttc, message.message_id)

        log.info("Succssfully unregistered")

    except Exception as e:
        log.error(f"Something went wrong while unregistering fin: {e}")
        send_nack(mqttc, message. message_id)


def unregister_capability(mqttc: mqtt.Client, message: Unregister, capabilities: list[CapabilityStructure]):
    try:
        capabilities[:] = [
            cap for cap in capabilities if cap.capability_id != message.capability_id]

        send_ack(mqttc, message.message_id)

        log.info("Succssfully unregistered")

    except Exception as e:
        log.error(f"Something went wrong while unregistering fin: {e}")
        send_nack(mqttc, message.message_id)
