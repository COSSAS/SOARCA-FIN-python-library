import os
import json
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
from paho.mqtt.subscribeoptions import SubscribeOptions
# Use uuid1 for non-safe uuids (uses address) and uuid4 for complete random
from uuid import uuid1
from concurrent.futures import ThreadPoolExecutor
from messageFactory import generateAckMessage, generateCapabilityStructureMessage, generateRegisterMessage
from messages.ackMessage import AckMessage
from messages.unRegisterMessage import UnRegisterMessage
from messages.capabilityStructureMessage import CapabilityStructureMessage


class SoarcaFin:

    def __init__(self, name: str):
        self.name = name
        self.fin_id = str(uuid1())
        self.thread_pool = ThreadPoolExecutor(max_workers=1)
        self.acks = {}
        self.capabilities: list[CapabilityStructureMessage] = []

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

        match FinRegisterFuture.exception(timeout=60):
            case None:
                print("Successfully registered fin")
            case Exception() as e:
                print(e)
                exit(-1)

        # Allow input to execute commands?
        while True:
            time.sleep(1)

        # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client: mqtt.Client, userdata, flags, reason_code, properties):

        print(f"Connected to the broker with result code {reason_code}")

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
        if not msg.payload:
            print("Empty payload")
            return
        content = ""
        try:
            content = json.loads(msg.payload.decode('utf8'))
        except Exception as e:
            print("Could not parse the payload as json format")
            print(e)

        if not "type" in content:
            print("Error, not message type found in payload")
            return

        match content["type"]:
            case "ack":
                on_ack_handler(self, content)
            case "nack":
                print("nack")
            case "register":
                print("skipping....")
            case "unregister":
                self.thread_pool.submit(on_unregister_handler, self, content)
            case _:
                print("error, no such command")

        # decoded = RegisterMessage(**json.loads(content))
        # print(content)
        # print(decoded)


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
    fin.mqttc.publish("soarca", json_msg, qos=1)

    fin.acks[msg.message_id] = "1"

    startTime = time.time()
    timeout = 60

    while time.time() < startTime + timeout:
        if not msg.message_id in fin.acks:
            print("received ack")
            return
        time.sleep(0.1)

    raise TimeoutError(
        f"Message with message id: {msg.message_id} was not acknowleged")


def on_ack_handler(fin: SoarcaFin, content: str):
    try:
        ack = AckMessage(**content)
        if ack.message_id in fin.acks:
            del fin.acks[ack.message_id]
        else:
            raise Exception(
                f"Ack with the message id: {ack.message_id} does not exist")
    except Exception as e:
        print(e)


def on_unregister_handler(fin: SoarcaFin, content: str):
    try:
        unregister = UnRegisterMessage(**content)
        if unregister.fin_id != fin.fin_id:
            print("Not the target fin, ignoring...")
            return
        if unregister.all:
            for capability in fin.capabilities:
                unregister_capability(
                    fin, capability.capability_id, unregister.message_id)
        else:
            unregister_capability(
                fin, unregister.capability_id, unregister.message_id)
    except Exception as e:
        print(e)


def unregister_capability(fin: SoarcaFin, id: str, message_id: str):
    if not id in fin.capabilities:
        raise Exception(f"Capability with id: {id} not recoginized")

    fin.capabilities = [
        cap for cap in fin.capabilities if cap.capability_id == id]

    ack = generateAckMessage(message_id)

    fin.mqttc.publish("soarca", payload=ack.toJson(), qos=1)


def main(username: str, password: str):
    fin = SoarcaFin("TestFin")
    fin.connect("localhost", 1883, username, password)


if __name__ == "__main__":
    try:
        load_dotenv()
        USERNAME = os.getenv("USERNAME")
        PASSWD = os.getenv("PASSWD")
    except Exception as e:
        print("Could not read environment variables. Make sure the .env file exists in the src directory")
        print(e)
        exit(-1)

    main(USERNAME, PASSWD)
