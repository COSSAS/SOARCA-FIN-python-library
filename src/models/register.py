from src.models.security import Security
from src.models.capabilityStructure import CapabilityStructure
from src.models.meta import Meta
from src.models.message import Message


class Register(Message):
    type: str = "register"
    # message_id: str implemented from parent
    fin_id: str
    protocol_version: str
    security: Security
    capabilities: list[CapabilityStructure]
    meta: Meta
