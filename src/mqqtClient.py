from __future__ import annotations
import logging as log
import paho.mqtt.client as mqtt

from handler import Handler
from dispatcher import Dispatcher
from messageFactory import generateRegisterMessage
from models.register import Register


class MqqtClient:

    def __init__(self, client: mqtt.Client, handler: Handler):
        self.client = client
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.dispatcher = Dispatcher(handler)
        self.handler = handler
        self.timeout = 20
        self.fin_id = "1"

    def on_connect(self, client: mqtt.Client, userdata, flags, reason_code, properties):

        log.debug(
            f"Connected to the broker with result code {reason_code}")

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        message = self.handler.handle_on_message(msg)
        if message:
            self.dispatcher.add_message(message)

    def register_fin(self, registerMessage: Register):
        self.dispatcher.add_message(registerMessage)
        self.dispatcher.start_dispatcher()
        # fn = self.handler.register_fin(self.fin_id)
        # future = self.executor.submit(fn)
        # match future.exception():
        #     case None:
        #         log.info("Successfully registered fin")
        #     case Exception() as e:
        #         log.critical(e)
        #         exit(-1)

    def unregister_fin(self):
        pass
        # fn = self.handler.unregister_fin()
        # self.executor.submit(fn)

    def unregister_capability(self, capability):
        pass
        # fn = self.handler.unregister_capability_command(capability)
        # self.executor.submit(fn)

    @classmethod
    def init_client_with_pw(cls, host: str, port: str, username: str, password: str) -> MqqtClient:
        mqttc = mqtt.Client(
            client_id="testFin", callback_api_version=mqtt.CallbackAPIVersion.VERSION2, clean_session=True)

        mqttc.username_pw_set(username, password)

        mqttc.connect(host, port, 60)

        # Start mqtt loop in background thread
        mqttc.loop_start()

        handler = Handler("1", "", mqttc)

        return MqqtClient(mqttc, handler)
