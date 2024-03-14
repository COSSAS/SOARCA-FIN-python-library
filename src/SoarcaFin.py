
from queue import Queue
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

    def create_fin_capability(self, capability: CapabilityStructure, callback) -> None:
        mqttc = self._create_mqtt_client(capability.capability_id)
        parser = Parser(capability.capability_id)
        executor = Executor(capability.capability_id, callback, Queue(), mqttc)
        capabilityClient = MQTTClient(
            capability.capability_id, mqttc, callback, executor, parser)
        self.capabilities[capability.capability_id] = capabilityClient
        self.capability_structure[capability.capability_id] = capability

    def set_config_MQTT_server(self, host: str, port: int, username: str, password: str) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def start_fin(self) -> None:
        for capability in self.capabilities.values():
            capability.start()

        mqttc = self._create_mqtt_client(self.fin_id)
        mqttc.subscribe(
            "soarca", options=SubscribeOptions(qos=1, noLocal=True))
        parser = Parser(self.fin_id)
        executor = Executor(self.fin_id, None, Queue(), mqttc)
        self.fin = MQTTClient(self.fin_id, mqttc, None, executor, parser)
        self.fin.start()
        register_msg = self._create_register_message()
        self.fin.executor.queue_message(register_msg)

    def _create_register_message(self) -> Register:
        msg_uuid = str(uuid1())
        security = Security(version="0.0.1", channel_security="plaintext")
        meta = Meta(timestamp="1234", sender_id=self.fin_id)
        return Register(message_id=msg_uuid, fin_id=self.fin_id, protocol_version="0.0.1",
                        security=security, capabilities=list(self.capability_structure.values()), meta=meta)

    def _create_mqtt_client(self, client_id: str) -> mqtt.Client:
        mqttc = mqtt.Client(
            client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2, protocol=PahoEnums.MQTTProtocolVersion.MQTTv5)

        mqttc.username_pw_set(self.username, self.password)

        mqttc.connect(self.host, self.port, 60)

        return mqttc
