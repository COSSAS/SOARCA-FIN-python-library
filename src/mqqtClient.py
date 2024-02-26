from __future__ import annotations
import json
import logging as log
import paho.mqtt.client as mqtt

from executor import Executor
from handler import Handler


class MqqtClient:

    def __init__(self, client: mqtt.Client, executor: Executor, handler: Handler):
        self.client = client
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.executor = executor
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
        fn = self.handler.handle_on_message(msg)
        if not fn:
            return
        self.executor.submit(fn)

    def register_fin(self):
        fn = self.handler.register_fin(self.fin_id)
        future = self.executor.submit(fn)
        match future.exception():
            case None:
                log.info("Successfully registered fin")
            case Exception() as e:
                log.critical(e)
                exit(-1)

    def unregister_fin(self):
        fn = self.handler.unregister_fin()
        self.executor.submit(fn)

    def unregister_capability(self, capability):
        fn = self.handler.unregister_capability_command(capability)
        self.executor.submit(fn)

    @classmethod
    def init_client_with_pw(cls, host: str, port: str, username: str, password: str) -> MqqtClient:
        mqttc = mqtt.Client(
            client_id="testFin", callback_api_version=mqtt.CallbackAPIVersion.VERSION2, clean_session=True)

        mqttc.username_pw_set(username, password)

        mqttc.connect(host, port, 60)

        # Start mqtt loop in background thread
        mqttc.loop_start()

        executor = Executor(1)
        handler = Handler("1", "", mqttc)

        return MqqtClient(mqttc, executor, handler)
