from messages.registerMessage import RegisterMessage
from messages.capabilityStructureMessage import CapabilityStructureMessage
from uuid import uuid1

from messages.ackMessage import AckMessage
from messages.nackMessage import NackMessage
from messages.resultMessage import ResultMessage
from messages.resultStructure import ResultStructureMessage
from messages.variableMessage import VariableMessage
from messages.agentStructureMessage import AgentStructureMessage
from messages.stepStructureMessage import StepStructureMessage
from messages.extrernalReferenceMessage import ExternalReferenceMessage


def generateRegisterMessage(fin_id) -> RegisterMessage:
    return RegisterMessage(fin_id=fin_id, message_id=str(uuid1()), protocol_version="1.0.0", security="", capabiltities=[], meta="")


def generateCapabilityStructureMessage(capability_id, name, step: any, agent: any) -> CapabilityStructureMessage:
    return CapabilityStructureMessage(capability_id=capability_id, type="empty", name=name, step=step, agent=agent, version="TODO")


def generateStepStructureMessage(type: str, name: str, description: str, external_references: ExternalReferenceMessage, command: str, target: str) -> StepStructureMessage:
    return StepStructureMessage(type, name, description, external_references, command, target)


def generateExternalReferenceMessage(name, description=None, url=None, external_id=None, reference_id=None) -> ExternalReferenceMessage:
    return ExternalReferenceMessage(name, description, url, external_id, reference_id)




def generateAckMessage(message_id: str) -> AckMessage:
    return AckMessage(message_id)


def generateNackMessage(message_id: str) -> NackMessage:
    return NackMessage(message_id)


def generateResultMessage(message_id: str, result: ResultStructureMessage, variables: dict[str, VariableMessage]) -> ResultMessage:
    return ResultMessage(message_id, result, variables, result)


def generateAgentStructureMessage(name: str, uuid: str) -> AgentStructureMessage:
    return AgentStructureMessage(name=f"soarca-fin--{name}-{uuid}")
