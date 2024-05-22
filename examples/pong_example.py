import os
from dotenv import load_dotenv

from soarca_fin_python_library.soarca_fin import SoarcaFin
from soarca_fin_python_library.models.agent_structure import AgentStructure
from soarca_fin_python_library.models.external_reference import ExternalReference
from soarca_fin_python_library.models.step_structure import StepStructure
from soarca_fin_python_library.models.capability_structure import CapabilityStructure
from soarca_fin_python_library.enums.workflow_step_enum import WorkFlowStepEnum
from soarca_fin_python_library.models.command import Command
from soarca_fin_python_library.models.result_structure import ResultStructure

from soarca_fin_python_library.models.variable import Variable
from soarca_fin_python_library.enums.variable_type_enum import VariableTypeEnum


def capability_pong_callback(command: Command) -> ResultStructure:
    print("Received ping, returning pong!")

    result = Variable(
        type=VariableTypeEnum.string,
        name="pong_output",
        description="If ping, return pong",
        value="pong",
        constant=True,
        external=False)

    context = command.command.context

    return ResultStructure(
        state="success", context=context, variables={"result": result})


def main(mqtt_broker: str, mqtt_port: int, username: str, password: str) -> None:

    finId = "soarca-fin--pingpong-f877bb3a-bb37-429e-8ece-2d4286cf326d"
    agentName = "soarca-fin-pong-f896bb3b-bb37-429e-8ece-2d4286cf326d"
    externalReferenceName = "external-reference-example-name"
    capabilityId = "mod-pong--e896aa3b-bb37-429e-8ece-2d4286cf326d"

    # Create AgentStructure
    agent = AgentStructure(
        name=agentName)

    # Create ExternalReference
    external_reference = ExternalReference(name=externalReferenceName)

    # Create StepStructure
    step_structure = StepStructure(
        name="step_name",
        description="step description",
        external_references=[external_reference],
        command="pong",
        target=agentName)

    # Create CapabilityStructure
    capability_structure = CapabilityStructure(
        capability_id=capabilityId,
        type=WorkFlowStepEnum.action,
        name="Ping Pong capability",
        version="0.0.1",
        step={
            "test": step_structure},
        agent={
            "testagent": agent})

    # Create Soarca fin
    fin = SoarcaFin(finId)
    # Set config for MQTT Server
    fin.set_config_MQTT_server(mqtt_broker, mqtt_port, username, password)
    # Register Capabilities
    fin.create_fin_capability(capability_structure, capability_pong_callback)
    # Start the fin
    fin.start_fin()


if __name__ == "__main__":
    load_dotenv()
    MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
    MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
    USERNAME = os.getenv("MQTT_USERNAME", "soarca")
    PASSWD = os.getenv("MQTT_PASSWD", "password")

    main(MQTT_BROKER, MQTT_PORT, USERNAME, PASSWD)
