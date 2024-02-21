from dataclasses import dataclass
import json
from messages.capabilityStructureMessage import CapabilityStructureMessage

@dataclass
class RegisterMessage:
    message_id: str
    fin_id: str
    protocol_version: str
    security: any
    capabiltities: list[CapabilityStructureMessage]
    meta: any
    type: str = "register"

    def toJson(self) -> str:
        jsondata = json.dumps(self, default=lambda o:o.__dict__, indent=4)
        return jsondata



