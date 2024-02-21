from messages.registerMessage import RegisterMessage
from messages.capabilityStructureMessage import CapabilityStructureMessage
from uuid import uuid1

from messages.ackMessage import AckMessage


def generateRegisterMessage(fin_id) -> RegisterMessage:
    return RegisterMessage(fin_id=fin_id, message_id=str(uuid1()), protocol_version="1.0.0", security="", capabiltities=[], meta="")


def generateCapabilityStructureMessage(capability_id, name, step: any, agent: any):
    return CapabilityStructureMessage(capability_id=capability_id, type="empty", name=name, step=step, agent=agent, version="1.0.1")


def generateAckMessage(message_id: str) -> AckMessage:
    return AckMessage(message_id)
