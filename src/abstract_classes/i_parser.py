from abc import ABC, abstractmethod
import paho.mqtt.client as mqtt
from src.models.message import Message


class IParser(ABC):

    @abstractmethod
    def parse_on_message(self, message: mqtt.MQTTMessage) -> Message:
        pass
