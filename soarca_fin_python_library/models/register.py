from soarca_fin_python_library.models.security import Security
from soarca_fin_python_library.models.capability_structure import CapabilityStructure
from soarca_fin_python_library.models.meta import Meta
from soarca_fin_python_library.models.message import Message


class Register(Message):
    type: str = "register"
    # message_id: str implemented from parent
    fin_id: str
    protocol_version: str
    security: Security
    capabilities: list[CapabilityStructure]
    meta: Meta
