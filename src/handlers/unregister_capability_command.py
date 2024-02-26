from uuid import uuid1
import paho.mqtt.client as mqtt
import logging as log
from messages.unRegisterMessage import UnRegisterMessage
from messages.capabilityStructureMessage import CapabilityStructureMessage


def unregister_capability_command(mqttc: mqtt.Client, capability: CapabilityStructureMessage, capabilities, ack_awaiter):
    try:
        msg_id = str(uuid1())
        msg = UnRegisterMessage(
            message_id=msg_id, capability_id=capability.capability_id)

        json_msg = msg.toJson()

        ack_awaiter(msg.message_id, lambda: mqttc.publish(
            "soarca", json_msg, qos=1))

        capabilities.remove(capability)

        log.info("Successfully unregistered")

    except Exception as e:
        log.error(f"Could not unregister: {e}")
