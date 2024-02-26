import paho.mqtt.client as mqtt
import logging as log

from handlers.send_ack import send_ack
from handlers.send_nack import send_nack


def unregister_fin_handler(mqttc: mqtt.Client, fin_id, message_id: str, capabilities):
    try:
        mqttc.unsubscribe(fin_id)
        mqttc.unsubscribe("soarca")
        for cap in capabilities:
            mqttc.unsubscribe(cap.capability_id)
        # Should we shut down the thread pool?

        send_ack(mqttc, message_id)

        log.info("Succssfully unregistered")

    except Exception as e:
        log.error(f"Something went wrong while unregistering fin: {e}")
        send_nack(mqttc, message_id)


def unregister_capability(mqttc: mqtt.Client, capability_id: str, message_id: str, capabilities):
    try:
        capabilities[:] = [
            cap for cap in capabilities if capability_id != capability_id]

        send_ack(mqttc, message_id)

        log.info("Succssfully unregistered")

    except Exception as e:
        log.error(f"Something went wrong while unregistering fin: {e}")
        send_nack(mqttc, message_id)
