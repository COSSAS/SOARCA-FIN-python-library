import os
import logging as log
import time
from uuid import uuid1
from dotenv import load_dotenv

from SoarcaFin import SoarcaFin
from models.security import Security
from models.agentStructure import AgentStructure
from models.externalReference import ExternalReference
from models.stepStructure import StepStructure
from models.capabilityStructure import CapabilityStructure
from enums.workFlowStepEnum import WorkFlowStepEnum
from models.result import Result
from models.command import Command
from models.meta import Meta
from models.resultStructure import ResultStructure
from models.context import Context
from datetime import datetime, timezone


def capability_test_callback(command: Command) -> Result:
    # See Ping:
    #   Send Pong back
    print("Capability callback")
    message_id = str(uuid1())
    timestamp = datetime.now(timezone.utc).isoformat()
    meta = Meta(timestamp=timestamp, sender_id="1234")
    context = Context(step_id="1", playbook_id="2", execution_id="3")
    resultstructure = ResultStructure(
        state="success", context=context, variables={})
    return Result(message_id=message_id, meta=meta, result=resultstructure)


def main(username: str, password: str) -> None:
    security = Security(version="0.0.1", channel_security="plaintext")

    agent = AgentStructure(name="soarca-fin--123")

    external_refernce = ExternalReference(name="external-reference-name")

    step_structure = StepStructure(name="step_name", description="step description",
                                   external_references=external_refernce, command="test-command", target="123456")

    capability_structure = CapabilityStructure(
        capability_id="mod-virustotal--e896aa3b-bb37-429e-8ece-2d4286cf326d", type=WorkFlowStepEnum.action, name="capability_name", version="0.0.1", step={"test": step_structure})

    # Create Soarca fin
    fin = SoarcaFin("123456789")
    # Set config for MQTT Server
    fin.set_config_MQTT_server("localhost", 1883, username, password)
    # Register Capabilities
    fin.create_fin_capability(capability_structure, capability_test_callback)
    # Start the fin
    fin.start_fin()


if __name__ == "__main__":
    log.basicConfig()
    log.getLogger().setLevel(log.DEBUG)
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
