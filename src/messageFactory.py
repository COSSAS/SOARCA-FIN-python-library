import datetime
from uuid import uuid1
from messages.resultMessage import ResultMessage
from messages.resultStructure import ResultStructureMessage
from messages.variableMessage import VariableMessage
from models.ack import Ack
from models.nack import Nack
from models.agentStructure import AgentStructure
from models.externalReference import ExternalReference
from models.stepStructure import StepStructure
from models.capabilityStructure import CapabilityStructure
from enums.workFlowStepEnum import WorkFlowStepEnum
from models.security import Security
from models.meta import Meta
from models.register import Register


def generateRegisterMessage(fin_id: str, protocol_version: str, security: Security, capabilitites: list[CapabilityStructure], meta: Meta = None, message_id=None) -> Register:
    message_id = message_id
    if not message_id:
        message_id = str(uuid1())

    meta = meta
    if not meta:
        meta = generateMetaMessage(fin_id)

    return Register(message_id=message_id, fin_id=fin_id,
                    protocol_version=protocol_version, security=security, capabilities=capabilitites, meta=meta)


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


def generateSecurityMessage(version: str, channel_security: str) -> Security:
    return Security(version=version, channel_security=channel_security)


def generateMetaMessage(sender_id: str, timestamp: str = None) -> Meta:
    timestamp = timestamp
    if not timestamp:
        timestamp = datetime.datetime.now().isoformat()
    return Meta(timestamp=timestamp, sender_id=sender_id)
