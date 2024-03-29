import json

from src.abstract_classes.i_parser import IParser
from src.models.ack import Ack
from src.models.message import Message
import paho.mqtt.client as mqtt
import logging as log

from src.models.nack import Nack
from src.models.unregister import Unregister
from src.models.command import Command

# Parser class to convert MQTT messages to Fin protocol messages.


class Parser(IParser):

    def __init__(self, id: str):
        self.id = id

    def parse_on_message(self, message: mqtt.MQTTMessage) -> Message:
        # Check if we did not receive an empty MQTT message.
        if not message.payload:
            log.error(f"Received a message with an empty payload")
            raise LookupError("Could not receive payload from message")
        content = ""
        # Try to convert MQTT payload to utf8 and load is as a JSON object.
        try:
            content = json.loads(message.payload.decode('utf8'))
        except Exception as e:
            log.error(f"Could not parse the payload as json format: {e}")
            raise e
        # Check for attribute 'type'. Is required to parse the message further.
        if "type" not in content:
            log.error("Error, no message type found in payload")
            raise LookupError("No type attribute in payload")

        # Check for attribute 'message_id'. Is required for a valid message.
        if "message_id" not in content:
            log.error("No message_id found in the payload")

        # Match on type and convert to Message types
        match content["type"]:
            case "ack":
                return Ack(**content)
            case "nack":
                return Nack(**content)
            case "command":
                return Command(**content)
            case "register":
                log.debug(
                    "Ignoring register request, since only the fin can start this")
            case "unregister":
                return Unregister(**content)
            case "result":
                log.debug(
                    "Ignoring result request, since only the fin can send this")
            case "unregister":
                # self.thread_pool.submit(on_unregister_handler, self, content)
                return Unregister(**content)
            case _:
                log.error("error, no such command")
