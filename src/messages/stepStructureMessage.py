from dataclasses import dataclass
import json
from dacite import from_dict
from messages.extrernalReferenceMessage import ExternalReferenceMessage


@dataclass
class StepStructureMessage:
    type: str
    name: str
    description: str
    external_references: ExternalReferenceMessage
    command: str
    target: str

    def toJson(self) -> str:
        jsondata = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        return jsondata

    def fromJson(content: str):
        return from_dict(StepStructureMessage, content)
