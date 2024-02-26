import json
import time
from enums.ackStatusEnum import AckStatus
from enums.timeoutStatusEnum import TimeoutStatus
import paho.mqtt.client as mqtt
import logging as log
from handlers.ack_handler import on_ack_handler
from handlers.register_fin import registerFin
from handlers.nack_handler import on_nack_handler
from messages.unRegisterMessage import UnRegisterMessage
from handlers.unregister_handlers import unregister_capability, unregister_fin_handler
from handlers.unregister_fin_command import unregister_fin_command
from handlers.unregister_capability_command import unregister_capability_command


class Handler:

    def __init__(self, fin_id: str, fin_name: str, mqttc):
        self.fin_id = fin_id
        self.fin_name = fin_name
        self.mqttc = mqttc
        self.capabilities = []
        self.acks: dict[str, AckStatus | TimeoutStatus] = {}
        self.TIMEOUT = 20

    def on_connect(self, reason_code):
        log.debug(
            f"Connected to the broker with result code {reason_code}")

    def handle_on_message(self, msg: mqtt.MQTTMessage):
        if not msg.payload:
            log.error(f"Received a message with an empty payload")
            return
        content = ""
        try:
            content = json.loads(msg.payload.decode('utf8'))
        except Exception as e:
            log.error(f"Could not parse the payload as json format: {e}")

        if not "type" in content:
            log.error("Error, not message type found in payload")
            return

        if not "message_id" in content:
            log.error("No message_id found in the payload")
            return

        if content["message_id"] in self.acks and not (content["type"] == "ack" or content["type"] == "nack"):
            log.debug("Received own message, skipping....")
            return

        match content["type"]:
            case "ack":
                self._handle_ack_case(content)
            case "nack":
                self._handle_nack_case(content)
                pass
            case "command":
                log.info("executing command")
            case "register":
                log.debug(
                    "Ignoring register request, since only the fin can start this")
            case "unregister":
                # self.thread_pool.submit(on_unregister_handler, self, content)
                self._handle_unregister_case(content)
            case _:
                log.error("error, no such command")

    def await_ack_with_func(self, message_id: str, callback):
        self.acks[message_id] = AckStatus.WAITING
        callback()
        while True:
            startTime = time.time()
            last_value = AckStatus.WAITING
            while time.time() < startTime + self.TIMEOUT:
                if self.acks[message_id] == AckStatus.SUCCESS:
                    log.debug("received ack")
                    del self.acks[message_id]
                    return
                if self.acks[message_id] == AckStatus.FAIL and not self.acks[message_id] == last_value:
                    log.error("Received NACK, attempting again...")
                    last_value = AckStatus.FAIL
                    callback()
                if self.acks[message_id] == AckStatus.FAIL2 and not self.acks[message_id] == last_value:
                    log.error("Received NACK 2 times, attempting again...")
                    last_value = AckStatus.FAIL2
                    callback()
                if self.acks[message_id] == AckStatus.FAIL3 and not self.acks[message_id] == last_value:
                    log.critical("Received NACK 3 times, exiting program")
                    last_value = AckStatus.FAIL3
                    exit(-1)
                time.sleep(0.1)

            match self.acks[message_id]:
                case AckStatus.WAITING:
                    self.acks[message_id] = TimeoutStatus.TIMEOUT
                    log.error(
                        f"Message with message id: {message_id} was not acknowleged, attempting again...")
                    callback()
                case AckStatus.FAIL | TimeoutStatus.TIMEOUT:
                    self.acks[message_id] = TimeoutStatus.TIMEOUT2
                    log.error(
                        f"Message with message id: {message_id} was not acknowleged twice, attempting again...")
                    callback()
                case AckStatus.FAIL2 | TimeoutStatus.TIMEOUT2:
                    log.critical(
                        f"Message with message id: {message_id} was not acknowleged, exiting now")
                    exit(-1)

    def _handle_ack_case(self, content) -> None:
        on_ack_handler(content, self.acks)

    def _handle_nack_case(self, content) -> None:
        on_nack_handler(content, self.acks)

    def _handle_unregister_case(self, content):
        try:
            unregister = UnRegisterMessage(**content)
            if unregister.all or unregister.fin_id == self.fin_id:
                # Shutdown on the thread?
                unregister_fin_handler(self.mqttc, unregister.message_id)
            elif any(cap.capability_id == unregister.capability_id for cap in self.capabilities):
                return lambda: unregister_capability(self.mqttc, unregister.capability_id, unregister.message_id, self.capabilities)
            else:
                log.debug("Not targeted for this fin")
        except Exception as e:
            log.error(e)

    def register_fin(self, fin_id):
        return lambda: registerFin(self.mqttc, fin_id, self.await_ack_with_func)

    def unregister_fin(self):
        return lambda: unregister_fin_command(self.mqttc, self.fin_id, self.capabilities, self.await_ack_with_func)

    def unregister_capability_command(self, capability):
        return lambda: unregister_capability_command(self.mqttc, capability, self.capabilities, self.await_ack_with_func)
