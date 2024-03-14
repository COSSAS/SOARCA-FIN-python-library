import os
from uuid import uuid1
from dotenv import load_dotenv
# Use uuid1 for non-safe uuids (uses address) and uuid4 for complete random
import logging as log
from mqqtClient import MqqtClient
from messageFactory import generateAgentStructureMessage, generateCapabilityStructureMessage, generateExternalReferenceMessage, generateRegisterMessage, generateSecurityMessage, generateStepStructureMessage
from models.capabilityStructure import CapabilityStructure
from models.security import Security
from enums.workFlowStepEnum import WorkFlowStepEnum


class SoarcaFin:

    def __init__(self, name: str, fin_id: str, protocol_version: str, security: Security):
        self.name: str = name
        self.fin_id: str = fin_id
        self.protocol_version: str = protocol_version
        self.security: Security = security
        self.capabilities: dict[str, (CapabilityStructure, function)] = {}
        self.mqttc: MqqtClient | None = None

    def start_mqtt_client(self, host: str, port: str, username: str, password: str):
        try:
            mqttc = MqqtClient.init_client_with_pw(
                host, port, username, password)
            self.mqttc = mqttc
        except Exception as e:
            log.error(f"Could not initialize mqtt client: {e}")
            exit(-1)

    def register_capability(self, capability: CapabilityStructure, callback) -> None:
        capability_id = capability.capability_id
        if capability_id in self.capabilities:
            raise Exception(f"Key with id {capability_id} already exists")

        self.capabilities[capability_id] = (capability, callback)

    def register_fin(self):
        capabilities = [cap for cap, _ in self.capabilities.values()]
        registerMessage = generateRegisterMessage(
            self.fin_id, self.protocol_version, self.security, capabilities)
        self.mqttc.register_fin(registerMessage)

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
    security_version = "0.0.1"
    channel_security = "plaintext"
    securityMessage = generateSecurityMessage(
        security_version, channel_security)

    agent_name = "test"
    uuid_agent = str(uuid1())
    agentStructure = generateAgentStructureMessage(agent_name, uuid_agent)

    ext_name = "test"
    externalReference = generateExternalReferenceMessage(ext_name)

    type = "action"
    step_name = "test step"
    description = "test description"
    command = "test command"
    target = str(uuid1())

    stepStructure = generateStepStructureMessage(
        type, step_name, description, [externalReference], command, target)

    capability_id = str(uuid1())
    type = WorkFlowStepEnum.action
    capability_name = "test name"
    version = "0.0.1"

    capabilityStructure = generateCapabilityStructureMessage(
        capability_id, type, capability_name, version, stepStructure, agentStructure)

    fin_id = "1"

    fin = SoarcaFin("TestFin", fin_id, protocol_version=version,
                    security=securityMessage)
    fin.start_mqtt_client("localhost", 1883, username, password)

    fin.register_capability(capabilityStructure, capability_callback_test)

    fin.register_fin()


def capability_callback_test():
    print("Test capability")


# if __name__ == "__main__":
#     log.basicConfig()
#     log.getLogger().setLevel(log.DEBUG)
#     try:
#         load_dotenv()
#         USERNAME = os.getenv("USERNAME")
#         PASSWD = os.getenv("PASSWD")
#     except Exception as e:
#         log.CRITICAL(
#             "Could not read environment variables. Make sure the .env file exists in the src directory")
#         log.CRITICAL(e)
#         exit(-1)

#     main(USERNAME, PASSWD)
