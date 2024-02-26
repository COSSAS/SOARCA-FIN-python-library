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
from messageFactory import generateAckMessage, generateCapabilityStructureMessage, generateNackMessage, generateRegisterMessage, generateResultMessage
from messages.ackMessage import AckMessage
from messages.unRegisterMessage import UnRegisterMessage
from messages.capabilityStructureMessage import CapabilityStructureMessage
from messages.nackMessage import NackMessage
from messages.commandMessage import CommandMessage
from messages.resultMessage import ResultMessage
from enums.ackStatusEnum import AckStatus
from enums.timeoutStatusEnum import TimeoutStatus
from mqqtClient import MqqtClient


class SoarcaFin:

    def __init__(self, name: str):
        self.name = name
        self.fin_id = "1"  # str(uuid1())
        self.thread_pool = ThreadPoolExecutor(max_workers=1)
        self.acks: dict[str, AckStatus | TimeoutStatus] = {}
        self.capabilities: list[CapabilityStructureMessage] = []
        self.TIMEOUT = 20
        self.mqttc: MqqtClient | None = None

    def start_mqtt_client(self, host: str, port: str, username: str, password: str):
        try:
            mqttc = MqqtClient.init_client_with_pw(
                host, port, username, password)
            self.mqttc = mqttc
        except Exception as e:
            log.error(f"Could not initialize mqtt client: {e}")
            exit(-1)

    def register_fin(self):

        self.mqttc.register_fin()

        # Allow input to execute commands?
        while True:
            command = input("Waiting for commands:\n1). Unregister\n\n")
            try:
                match int(command):
                    case 1:
                        self.unregister_command()
                    case _:
                        print(
                            "Command unkown, please choose a valid option from the options screen\n\n")

            except Exception as e:
                print("Not a valid input\n\n")

        # The callback for when the client receives a CONNACK response from the server.


# def on_command_handler(fin: SoarcaFin, content: str):
#     try:
#         command = CommandMessage(**content)
#         send_ack(fin, command.message_id)

#         log.info("Executing command...")

#         result = execute_command(fin, command)

#         ack_awaiter(fin, command.message_id,
#                     lambda: fin.mqttc.publish(fin.fin_id, result.toJson(), qos=1))

#     except Exception as e:
#         log.error(f"Could not parse or execute the command error: {e}")


# def execute_command(fin: SoarcaFin, command: CommandMessage) -> ResultMessage:

#     # TODO: Check authentication

#     subCommand = command.command

#     result = generateResultMessage(command)

    def unregister_command(self):
        print("Which fin or capability should be unregistered:")
        print("0). Cancel")
        print(f"1). Fin ({self.fin_id})")
        for i, cap in enumerate(self.capabilities):
            print("{}). Capabiltity {} ({})".format(
                i+2, cap.name, cap.capability_id))
        command = input("\n")
        try:
            match int(command):
                case 0:
                    return
                case 1:
                    self.mqttc.unregister_fin()
                case _ if int(command) < len(self.capabilities) + 2:
                    capability = self.capabilities[int(command) - 2]

                    self.mqttc.unregister_capability(capability)
                case _:
                    print("")
        except Exception as e:
            print("Not a valid input\n\n")


def main(username: str, password: str):
    fin = SoarcaFin("TestFin")
    fin.start_mqtt_client("localhost", 1883, username, password)
    fin.register_fin()


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
