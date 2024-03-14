import json

from abstract_classes.IParser import IParser
from models.ack import Ack
from models.message import Message
import paho.mqtt.client as mqtt
import logging as log

from models.nack import Nack
from models.unregister import Unregister
from models.command import Command


class Parser(IParser):

    def __init__(self, id: str):
        self.id = id

    def parse_on_message(self, message: mqtt.MQTTMessage) -> Message:
        if not message.payload:
            log.error(f"Received a message with an empty payload")
            raise LookupError("Could not receive payload from message")
        content = ""
        try:
            content = json.loads(message.payload.decode('utf8'))
        except Exception as e:
            log.error(f"Could not parse the payload as json format: {e}")
            raise e
        if not "type" in content:
            log.error("Error, no message type found in payload")
            raise LookupError("No type attribute in payload")

        if not "message_id" in content:
            log.error("No message_id found in the payload")

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
