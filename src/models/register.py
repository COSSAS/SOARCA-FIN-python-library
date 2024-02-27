from models.security import Security
from models.capabilityStructure import CapabilityStructure
from models.meta import Meta
from models.message import Message


class Register(Message):
    type: str = "register"
    # message_id: str implemented from parent
    fin_id: str
    protocol_version: str
    security: Security
    capabilities: list[CapabilityStructure]
    meta: Meta
