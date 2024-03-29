import os
import logging as log
from dotenv import load_dotenv

from soarca_fin_python_library.soarca_fin import SoarcaFin
from soarca_fin_python_library.models.security import Security
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
    log.info("Received ping, returning pong!")
    out = Variable(
        type=VariableTypeEnum.string,
        name="pong_output",
        description="If ping, return pong",
        value="pong",
        constant=True,
        external=False)
    context = command.command.context
    return ResultStructure(
        state="success", context=context, variables={"result": out})


def main(username: str, password: str) -> None:
    security = Security(version="0.0.1", channel_security="plaintext")

    agent = AgentStructure(name="soarca-fin--123")

    external_refernce = ExternalReference(name="external-reference-name")

    step_structure = StepStructure(
        name="step_name",
        description="step description",
        external_references=external_refernce,
        command="test-command",
        target="123456")

    capability_structure = CapabilityStructure(
        capability_id="mod-virustotal--e896aa3b-bb37-429e-8ece-2d4286cf326d",
        type=WorkFlowStepEnum.action,
        name="capability_name",
        version="0.0.1",
        step={
            "test": step_structure},
        agent={
            "testagent": agent})

    # Create Soarca fin
    fin = SoarcaFin("123456789")
    # Set config for MQTT Server
    fin.set_config_MQTT_server("localhost", 1883, username, password)
    # Register Capabilities
    fin.create_fin_capability(capability_structure, capability_pong_callback)
    # Start the fin
    fin.start_fin()


if __name__ == "__main__":
    log.basicConfig()
    log.getLogger().setLevel(log.DEBUG)
    try:
        load_dotenv()
        USERNAME = os.getenv("MQTT_USERNAME")
        PASSWD = os.getenv("MQTT_PASSWD")
    except Exception as e:
        log.critical(
            "Could not read environment variables. Make sure the .env file exists in the src directory")
        log.critical(e)
        exit(-1)

    main(USERNAME, PASSWD)