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

    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        message = self.handler.handle_on_message(msg)
        if message:
            self.dispatcher.add_message(message)

    def register_fin(self, registerMessage: Register):
        self.dispatcher.start_dispatcher()
        self.dispatcher.add_message(registerMessage)

        # Wait for dispatcher to proccess register message
        self.dispatcher.block_until_task_done(registerMessage.message_id)
        log.info("Successfully registered fin")

    def unregister_fin(self):
        pass

    def unregister_capability(self, capability):
        pass

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
