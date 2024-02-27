from messages.registerMessage import RegisterMessage
from messages.capabilityStructureMessage import CapabilityStructureMessage
from uuid import uuid1
from messages.resultMessage import ResultMessage
from messages.resultStructure import ResultStructureMessage
from messages.variableMessage import VariableMessage
from messages.extrernalReferenceMessage import ExternalReferenceMessage
from models.ack import Ack
from models.nack import Nack
from models.agentStructure import AgentStructure
from models.externalReference import ExternalReference
from models.stepStructure import StepStructure
from models.capabilityStructure import CapabilityStructure
from enums.workFlowStepEnum import WorkFlowStepEnum


def generateRegisterMessage(fin_id) -> RegisterMessage:
    return RegisterMessage(fin_id=fin_id, message_id=str(uuid1()), protocol_version="1.0.0", security="", capabiltities=[], meta="")


def generateCapabilityStructureMessage(capability_id: str, type: WorkFlowStepEnum, name: str, version: str, step: StepStructure, agent: AgentStructure) -> CapabilityStructure:
    return CapabilityStructure(capability_id=capability_id, type=type, name=name, step=step, agent=agent, version=version)


def generateStepStructureMessage(type: str, name: str, description: str, external_references: list[ExternalReference], command: str, target: str) -> StepStructure:
    return StepStructure(type=type, name=name, description=description, external_references=external_references, command=command, target=target)


def generateExternalReferenceMessage(name: str, description: str = None, source: str = None, url: str = None, external_id: str = None, reference_id: str = None) -> ExternalReference:
    return ExternalReference(name=name, description=description, source=source, url=url, external_id=external_id, reference_id=reference_id)


def generateAckMessage(message_id: str) -> Ack:
    return Ack(message_id=message_id)


def generateNackMessage(message_id: str) -> Nack:
    return Nack(message_id=message_id)


def generateResultMessage(message_id: str, result: ResultStructureMessage, variables: dict[str, VariableMessage]) -> ResultMessage:
    return ResultMessage(message_id, result, variables, result)


def generateAgentStructureMessage(name: str, uuid: str) -> AgentStructure:
    return AgentStructure(name=f"soarca-fin--{name}-{uuid}")
