import threading
import logging as log
from paho.mqtt.client import Client, ConnectFlags, MQTTMessage
from paho.mqtt.properties import Properties
from paho.mqtt.reasoncodes import ReasonCode
import paho.mqtt.client as mqtt
from paho.mqtt.subscribeoptions import SubscribeOptions

from soarca_fin_python_library.abstract_classes.i_executor import IExecutor
from soarca_fin_python_library.abstract_classes.i_parser import IParser
from soarca_fin_python_library.abstract_classes.i_mqtt_client import IMQTTClient
from soarca_fin_python_library import Executor


class MQTTClient(IMQTTClient):

    def __init__(
            self,
            id: str,
            mqttc: mqtt.Client,
            callback,
            executor: IExecutor,
            parser: IParser):
        self.id: str = id
        self.mqttc: mqtt.Client = mqttc
        self.callback = callback
        self.executor: Executor = executor
        self.parser = parser
        self._executor_thread = None

    # On connect callback function for Paho MQTT client
    def on_connect(
            self,
            client: Client,
            userdata,
            connect_flags: ConnectFlags,
            reason_code: ReasonCode,
            properties: Properties):
        return

    # On message callback function for Paho MQTT client
    def on_message(self, client: Client, userdata, message: MQTTMessage):
        try:
            # Parse message to check message type
            msg = self.parser.parse_on_message(message)
            # If we should process the message, send it to the executor
            if msg:
                self.executor.queue_message(msg)
        except Exception as e:
            log.error(f"Something went wrong when parsing messag:\n{e}")

    # Start the MQTT client by registering mqtt callbacks, subscribing to
    # topic and launching executor
    def start(self):
        # Set mqttc callback functions
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

        # Subscribe to capability topic using noLocal (requires MQTTv5).
        # noLocal is used to not receive own messages such as Acks.
        self.mqttc.subscribe(
            self.id, options=SubscribeOptions(qos=1, noLocal=True))

        # Start callback loops for mqtt in the background
        self.mqttc.loop_start()

        # Start executor thread
        self._executor_thread = threading.Thread(
            target=self.executor.start_executor,
            name=f"executor-thread-{self.id}")
        self._executor_thread.daemon = True

        self._executor_thread.start()

    # Stop MQTT client by unsubscribing, stopping mqtt callbacks and exiting
    # executor
    def stop(self):
        self.mqttc.unsubscribe(self.id)
        self.mqttc.loop_stop()
        self.executor.stop_executor()
