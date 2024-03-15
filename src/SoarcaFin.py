
from queue import Queue
import time
from uuid import uuid1
import paho.mqtt.client as mqtt
import paho.mqtt.enums as PahoEnums
from abstract_classes.ISoarcaFin import ISoarcaFin
from abstract_classes.IMQTTClient import IMQTTClient
from models.capabilityStructure import CapabilityStructure
from paho.mqtt.subscribeoptions import SubscribeOptions
from MQTTClient import MQTTClient
from Parser import Parser
from Executor import Executor
from models.register import Register
from models.security import Security
from models.meta import Meta
from models.message import Message
from models.unregister import Unregister
import logging as log

from models.unregisterSelf import UnregisterSelf
from models import unregisterSelf


class SoarcaFin(ISoarcaFin):

    def __init__(self, fin_id: str):
        self.fin_id: str = fin_id
        self.host: str = None
        self.port: int = None
        self.username: str = None
        self.password: str = None
        self.capabilities: dict[str, IMQTTClient] = {}
        self.capability_structure: dict[str, CapabilityStructure] = {}
        self.fin: IMQTTClient = None

    # Create a soarca capability by listing on a topic and registering callback function
    def create_fin_capability(self, capability: CapabilityStructure, callback) -> None:
        mqttc = self._create_mqtt_client(capability.capability_id)
        parser = Parser(capability.capability_id)
        executor = Executor(capability.capability_id, callback, Queue(), mqttc)
        capabilityClient = MQTTClient(
            capability.capability_id, mqttc, callback, executor, parser)
        self.capabilities[capability.capability_id] = capabilityClient
        self.capability_structure[capability.capability_id] = capability

    # Set settings for MQTT Server
    def set_config_MQTT_server(self, host: str, port: int, username: str, password: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    # Starts the fin and the capabilities by sending a register message to the MQTT broker
    # on the 'soarca' topic.
    def start_fin(self) -> None:
        # Start the capabilities so they can listen for incomming messages immediately
        for capability in self.capabilities.values():
            capability.start()

        # Create fin control MQTT client to handle all control functions
        mqttc = self._create_mqtt_client(self.fin_id)
        mqttc.subscribe(
            "soarca", options=SubscribeOptions(qos=1, noLocal=True))
        parser = Parser(self.fin_id)
        executor = Executor(
            self.fin_id, self.fin_control_callback, Queue(), mqttc)
        self.fin = MQTTClient(self.fin_id, mqttc, None, executor, parser)

        # Start the control fin
        self.fin.start()

        # Send register message to the MQTT broker
        register_msg = self._create_register_message()
        self.fin.executor.queue_message(register_msg)
        self.fin._executor_thread.join()

    # Callback function for the control fin such that is can control the
    # capability fins
    def fin_control_callback(self, message: Message):
        match message:
            case Unregister() | UnregisterSelf():
                if message.all or message.fin_id == self.fin:
                    for capability in self.capabilities.values():
                        capability.stop()
                    self.fin.stop()
                    log.warn("Stopping in 10 seconds...")
                    time.sleep(10)
                elif message.capability_id in self.capabilities:
                    self.capabilities[message.capability_id].stop()
                    del self.capabilities[message.capability_id]
                    del self.capability_structure[message.capability_id]
                    log.warn(
                        f"Stopping capability with id {message.capability_id} in 10 seconds...")
                    time.sleep(10)
                else:
                    log.debug("Unregister not for this fin")
            case _:
                log.error("Unknown message")

    # Helper function to generate a register message from  registered capabilities
    def _create_register_message(self) -> Register:
        msg_uuid = str(uuid1())
        security = Security(version="0.0.1", channel_security="plaintext")
        meta = Meta(timestamp="1234", sender_id=self.fin_id)
        return Register(message_id=msg_uuid, fin_id=self.fin_id, protocol_version="0.0.1",
                        security=security, capabilities=list(self.capability_structure.values()), meta=meta)

    # Helper function to generate MQTT clients
    def _create_mqtt_client(self, client_id: str) -> mqtt.Client:
        mqttc = mqtt.Client(
            client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2, protocol=PahoEnums.MQTTProtocolVersion.MQTTv5)

        mqttc.username_pw_set(self.username, self.password)

        mqttc.connect(self.host, self.port, 60)

        return mqttc
