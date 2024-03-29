from abc import ABC, abstractmethod
from paho.mqtt.client import Client, MQTTMessage, ConnectFlags
from paho.mqtt.reasoncodes import ReasonCode
from paho.mqtt.properties import Properties


class IMQTTClient(ABC):

    @abstractmethod
    def on_connect(self, client: Client,
                   userdata,
                   connect_flags: ConnectFlags,
                   reason_code: ReasonCode,
                   properties: Properties):
        pass

    @abstractmethod
    def on_message(self, client: Client, userdata, message: MQTTMessage):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
