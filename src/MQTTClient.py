import threading
from paho.mqtt.client import Client, ConnectFlags, MQTTMessage
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode
from abstract_classes.IMQTTClient import IMQTTClient
import paho.mqtt.client as mqtt
from paho.mqtt.subscribeoptions import SubscribeOptions

from abstract_classes.IExecutor import IExecutor
from abstract_classes.IParser import IParser
import logging as log

from Executor import Executor


class MQTTClient(IMQTTClient):

    def __init__(self, id: str, mqttc: mqtt.Client, callback, executor: IExecutor, parser: IParser):
        self.id: str = id
        self.mqttc: mqtt.Client = mqttc
        self.callback = callback
        self.executor: Executor = executor
        self.parser = parser
        self._executor_thread = None

    def on_connect(self, client: Client, userdata, connect_flags: ConnectFlags, reason_code: ReasonCode, properties: Properties):
        return

    def on_message(self, client: Client, userdata, message: MQTTMessage):
        msg = self.parser.parse_on_message(message)

        if msg:
            self.executor.queue_message(msg)

    def start(self):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

        self.mqttc.subscribe(
            self.id, options=SubscribeOptions(qos=1, noLocal=True))

        self.mqttc.loop_start()

        self._executor_thread = threading.Thread(
            target=self.executor.start_executor, name=f"executor-thread-{self.id}")
        self._executor_thread.daemon = True

        self._executor_thread.start()
