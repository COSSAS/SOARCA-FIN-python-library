from uuid import uuid1
import paho.mqtt.client as mqtt
import logging as log
from messages.unRegisterMessage import UnRegisterMessage


def unregister_fin_command(mqttc: mqtt.Client, fin_id: str, capabilities, ack_awaiter):
    try:
        msg_id = str(uuid1())
        msg = UnRegisterMessage(message_id=msg_id, fin_id=fin_id)

        json_msg = msg.toJson()

        ack_awaiter(msg.message_id, lambda:
                    mqttc.publish("soarca", json_msg, qos=1))

        mqttc.unsubscribe(fin_id)
        mqttc.unsubscribe("soarca")
        for cap in capabilities:
            mqttc.unsubscribe(cap.capability_id)
        # Should we shut down the thread pool?

        log.info("Successfully unregistered")

    except Exception as e:
        log.error(f"Could not unregister: {e}")
