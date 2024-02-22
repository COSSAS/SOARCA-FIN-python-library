import os
import json
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from paho.mqtt.subscribeoptions import SubscribeOptions
# Use uuid1 for non-safe uuids (uses address) and uuid4 for complete random
from uuid import uuid1
from enum import Enum
import logging as log
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from messageFactory import generateAckMessage, generateCapabilityStructureMessage, generateNackMessage, generateRegisterMessage
from messages.ackMessage import AckMessage
from messages.unRegisterMessage import UnRegisterMessage
from messages.capabilityStructureMessage import CapabilityStructureMessage
from messages.nackMessage import NackMessage


class AckStatus(Enum):
    WAITING = 0
    SUCCESS = 1
    FAIL = 2
    FAIL2 = 3
    FAIL3 = 4


class TimeoutStatus(Enum):
    TIMEOUT = 2
    TIMEOUT2 = 3
    TIMEOUTU3 = 4


class SoarcaFin:

    def __init__(self, name: str):
        self.name = name
        self.fin_id = "1"  # str(uuid1())
        self.thread_pool = ThreadPoolExecutor(max_workers=1)
        self.acks: dict[str, AckStatus | TimeoutStatus] = {}
        self.capabilities: list[CapabilityStructureMessage] = []
        self.TIMEOUT = 20

    def connect(self, host, port, username, password):
        self.mqttc = mqtt.Client(
            client_id="testFin", callback_api_version=mqtt.CallbackAPIVersion.VERSION2, clean_session=True)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message

        self.mqttc.username_pw_set(username, password)

        self.mqttc.connect(host, port, 60)

        # Start mqtt loop in background thread
        self.mqttc.loop_start()

        FinRegisterFuture = self.thread_pool.submit(registerFin, self)

        match FinRegisterFuture.exception():
            case None:
                log.info("Successfully registered fin")
            case Exception() as e:
                log.critical(e)
                exit(-1)

        # Allow input to execute commands?
        while True:
            command = input("Waiting for commands:\n1). Unregister\n\n")
            try:
                match int(command):
                    case 1:
                        unregister_command(self)
                    case _:
                        print(
                            "Command unkown, please choose a valid option from the options screen\n\n")

            except Exception as e:
                print("Not a valid input\n\n")

        # The callback for when the client receives a CONNACK response from the server.

    def on_connect(self, client: mqtt.Client, userdata, flags, reason_code, properties):

        log.debug(f"Connected to the broker with result code {reason_code}")

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
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
                on_ack_handler(self, content)
            case "nack":
                on_nack_handler(self, content)
            case "register":
                log.debug(
                    "Ignoring register request, since only the fin can start this")
            case "unregister":
                self.thread_pool.submit(on_unregister_handler, self, content)
            case _:
                log.error("error, no such command")


def ack_awaiter(fin: SoarcaFin, message_id: str, callback):
    fin.acks[message_id] = AckStatus.WAITING
    callback()

    while True:
        startTime = time.time()

        while time.time() < startTime + fin.TIMEOUT:
            if fin.acks[message_id] == AckStatus.SUCCESS:
                log.debug("received ack")
                del fin.acks[message_id]
                return
            if fin.acks[message_id] == AckStatus.FAIL:
                log.debug("Received NACK, attempting again...")
                callback()
            if fin.acks[message_id] == AckStatus.FAIL2:
                log.debug("Received NACK 2 times, attempting again...")
                callback()
            if fin.acks[message_id] == AckStatus.FAIL3:
                log.critical("Received NACK 3 times, exiting program")
                exit(-1)
            time.sleep(0.1)

        match fin.acks[message_id]:
            case AckStatus.WAITING:
                fin.acks[message_id] = TimeoutStatus.TIMEOUT
                log.debug(
                    f"Message with message id: {message_id} was not acknowleged, attempting again...")
                callback()
            case AckStatus.FAIL | TimeoutStatus.TIMEOUT:
                fin.acks[message_id] = TimeoutStatus.TIMEOUT2
                log.debug(
                    f"Message with message id: {message_id} was not acknowleged twice, attempting again...")
                callback()
            case AckStatus.FAIL2 | TimeoutStatus.TIMEOUT2:
                log.debug(
                    f"Message with message id: {message_id} was not acknowleged, exiting now")
                exit(-1)


def registerFin(fin: SoarcaFin):
    # noLocal:            True or False. If set to True, the subscriber will not receive its own publications.
    # Does not seem to work
    fin.mqttc.subscribe(
        "soarca", options=SubscribeOptions(qos=1, noLocal=True))

    x = generateCapabilityStructureMessage(str(uuid1()), "cap1", "", "")
    msg = generateRegisterMessage(fin.fin_id)
    msg.capabiltities.append(x)
    fin.capabilities.append(x)
    json_msg = msg.toJson()

    fin.mqttc.subscribe(
        fin.fin_id, options=SubscribeOptions(qos=1, noLocal=True))

    ack_awaiter(fin, msg.message_id, lambda:
                fin.mqttc.publish("soarca", json_msg, qos=1))


def unregister_command(fin: SoarcaFin):
    print("Which fin or capability should be unregistered:")
    print("0). Cancel")
    print(f"1). Fin ({fin.fin_id})")
    for i, cap in enumerate(fin.capabilities):
        print("{}). Capabiltity {} ({})".format(
            i+2, cap.name, cap.capability_id))
    command = input("\n")
    try:
        match int(command):
            case 0:
                return
            case 1:
                on_unregister_fin_command(fin)
            case _ if int(command) < len(fin.capabilities) + 2:
                capability = fin.capabilities[int(command) - 2]

                on_unregister_capability_command(fin, capability)
            case _:
                print("")
    except Exception as e:
        print("Not a valid input\n\n")


def on_unregister_fin_command(fin: SoarcaFin):
    try:
        msg_id = str(uuid1())
        msg = UnRegisterMessage(message_id=msg_id, fin_id=fin.fin_id)

        json_msg = msg.toJson()

        ack_awaiter(fin, msg.message_id, lambda:
                    fin.mqttc.publish("soarca", json_msg, qos=1))

        fin.mqttc.unsubscribe(fin.fin_id)
        fin.mqttc.unsubscribe("soarca")
        for cap in fin.capabilities:
            fin.mqttc.unsubscribe(cap.capability_id)
        # Should we shut down the thread pool?
        fin.thread_pool.shutdown()

        log.info("Successfully unregistered")

    except Exception as e:
        log.error(f"Could not unregister: {e}")


def on_unregister_capability_command(fin: SoarcaFin, capability: CapabilityStructureMessage):
    try:
        msg_id = str(uuid1())
        msg = UnRegisterMessage(
            message_id=msg_id, capability_id=capability.capability_id)

        json_msg = msg.toJson()

        ack_awaiter(fin, msg.message_id, lambda: fin.mqttc.publish(
            "soarca", json_msg, qos=1))

        fin.capabilities.remove(capability)

        log.info("Successfully unregistered")

    except Exception as e:
        log.error(f"Could not unregister: {e}")


def on_ack_handler(fin: SoarcaFin, content: str):
    try:
        ack = AckMessage(**content)
        if ack.message_id in fin.acks:
            fin.acks[ack.message_id] = AckStatus.SUCCESS
        else:
            raise Exception(
                f"Ack with the message id: {ack.message_id} does not exist")
    except Exception as e:
        log.error(f"{e}")


def on_nack_handler(fin: SoarcaFin, content: str):
    try:
        ack = NackMessage(**content)
        if ack.message_id in fin.acks:
            match fin.acks[ack.message_id]:
                case AckStatus.WAITING:
                    fin.acks[ack.message_id] = AckStatus.FAIL
                case AckStatus.FAIL | TimeoutStatus.TIMEOUT:
                    fin.acks[ack.message_id] = AckStatus.FAIL2
                case AckStatus.FAIL2 | TimeoutStatus.TIMEOUTU3:
                    fin.acks[ack.message_id] = AckStatus.FAIL3
        else:
            raise Exception(
                f"Nack with the message id: {ack.message_id} does not exist")
    except Exception as e:
        log.error(f"{e}")


def on_unregister_handler(fin: SoarcaFin, content: str):
    try:
        unregister = UnRegisterMessage(**content)
        if unregister.all or unregister.fin_id == fin.fin_id:
            unregister_fin_handler(fin, unregister.message_id)
        elif any(cap.capability_id == unregister.capability_id for cap in fin.capabilities):
            unregister_capability(fin, unregister.message_id)
        else:
            log.debug("Not targeted for this fin")
    except Exception as e:
        log.error(e)


def unregister_fin_handler(fin: SoarcaFin, message_id: str):
    try:
        fin.mqttc.unsubscribe(fin.fin_id)
        fin.mqttc.unsubscribe("soarca")
        for cap in fin.capabilities:
            fin.mqttc.unsubscribe(cap.capability_id)
        # Should we shut down the thread pool?
        fin.thread_pool.shutdown()

        send_ack(fin, message_id)

        log.info("Succssfully unregistered")

    except Exception as e:
        log.error(f"Something went wrong while unregistering fin: {e}")
        send_nack(fin, message_id)


def unregister_capability(fin: SoarcaFin, capability_id: str, message_id: str):
    try:
        fin.capabilities = [
            cap for cap in fin.capabilities if cap.capability_id != capability_id]

        send_ack(fin, message_id)

        log.info("Succssfully unregistered")

    except Exception as e:
        log.error(f"Something went wrong while unregistering fin: {e}")
        send_nack(fin, message_id)


def send_ack(fin: SoarcaFin, message_id: str):
    ack = generateAckMessage(message_id)

    fin.mqttc.publish("soarca", payload=ack.toJson(), qos=1)


def send_nack(fin: SoarcaFin, message_id: str):
    nack = generateNackMessage(message_id)

    fin.mqttc.publish("soarca", payload=nack.toJson(), qos=1)


def main(username: str, password: str):
    fin = SoarcaFin("TestFin")
    fin.connect("localhost", 1883, username, password)


if __name__ == "__main__":
    try:
        load_dotenv()
        USERNAME = os.getenv("USERNAME")
        PASSWD = os.getenv("PASSWD")
    except Exception as e:
        log.CRITICAL(
            "Could not read environment variables. Make sure the .env file exists in the src directory")
        log.CRITICAL(e)
        exit(-1)

    main(USERNAME, PASSWD)
