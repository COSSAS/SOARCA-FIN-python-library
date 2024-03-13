from abc import ABC, abstractmethod
from paho.mqtt.client import Client, MQTTMessage, ConnectFlags
from paho.mqtt.reasoncodes import ReasonCode
from paho.mqtt.properties import Properties


class IHandler(ABC):

    @abstractmethod
    def on_connect(client: Client, userdata, connect_flags: ConnectFlags, reason_code: ReasonCode, properties: Properties):
        pass

    @abstractmethod
    def on_message(client: Client, userdata, message: MQTTMessage):
        pass
