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
from models.unregister import Unregister
from models.variable import Variable
from enums.variableTypeEnum import VariableTypeEnum
from models.context import Context
from enums.openVocabEnum import OpenVocabEnum
from models.authenticationInformation import AuthenticationInformation
from models.commandSubStructure import CommandSubStructure
from models.command import Command
from models.resultStructure import ResultStructure
from models.result import Result


def generateRegisterMessage(fin_id: str, protocol_version: str, security: Security, capabilitites: list[CapabilityStructure], meta: Meta = None, message_id=None) -> Register:
    message_id = message_id
    if not message_id:
        message_id = str(uuid1())

    meta = meta
    if not meta:
        meta = generateMetaMessage(fin_id)

    return Register(message_id=message_id, fin_id=fin_id,
                    protocol_version=protocol_version, security=security, capabilities=capabilitites, meta=meta)


def generateUnregisterMessage(all: bool = False, capability_id: str = None, fin_id: str = None, message_id: str = None) -> Unregister:

    message_id = message_id
    if not message_id:
        message_id = str(uuid1())

    if all:
        return Unregister(message_id=message_id, capability_id=None, fin_id=None, all=True)
    if capability_id:
        return Unregister(message_id=message_id, capability_id=capability_id, fin_id=None, all=False)
    if fin_id:
        return Unregister(message_id=message_id, capability_id=None, fin_id=fin_id, all=False)

    raise ValueError(
        "Either capability_id != null, fin_id != null or all == true need to be set")


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


def generateResultStructureMessage(state: str, context: Context, variables: dict[str, Variable]) -> ResultStructure:
    return ResultStructure(state=state, context=context, variables=variables)


def generateResultMessage(result: ResultStructure, meta: Meta, message_id: str = None) -> Result:
    message_id = message_id
    if not message_id:
        message_id = str(uuid1())
    return Result(message_id=message_id, result=result, meta=meta)


def generateAgentStructureMessage(name: str, uuid: str) -> AgentStructure:
    return AgentStructure(name=f"soarca-fin--{name}-{uuid}")


def generateSecurityMessage(version: str, channel_security: str) -> Security:
    return Security(version=version, channel_security=channel_security)


def generateMetaMessage(sender_id: str, timestamp: str = None) -> Meta:
    timestamp = timestamp
    if not timestamp:
        timestamp = datetime.datetime.now().isoformat()
    return Meta(timestamp=timestamp, sender_id=sender_id)


def generateVariableMessage(type: VariableTypeEnum, description: str, value: str, constant: bool, external: bool) -> Variable:
    return Variable(type=type, description=description, value=value, constant=constant, external=external)


def generateContextMessage(step_id: str, playbook_id: str, execution_id: str, completed_on: str = None, generated_on: str = None, timeout: str = None) -> Context:
    return Context(step_id=step_id, playbook_id=playbook_id, execution_id=execution_id, completed_on=completed_on, generated_on=generated_on, timeout=timeout)


def generateAuthenticationInformationMessage(type: OpenVocabEnum, name: str = None, description: str = None, authentication_info_extenstion: dict[str, str] = None) -> AuthenticationInformation:
    return AuthenticationInformation(type=type, name=name, description=description, authentication_info_extensions=authentication_info_extenstion)


def generateCommandSubStructureMessage(command: str, context: Context, variables: dict[str, Variable], authentication: dict[str, AuthenticationInformation] = None) -> CommandSubStructure:
    return CommandSubStructure(command=command, authentication=authentication, context=context, variables=variables)


def generateCommandMessage(command: CommandSubStructure, meta: Meta, message_id: str = None) -> Command:
    message_id = message_id
    if not message_id:
        message_id = str(uuid1())

    return Command(message_id=message_id, command=command, meta=meta)
