import json
from dataclasses import dataclass

from dacite import from_dict


@dataclass
class ExternalReferenceMessage:
    name: str
    description: str | None = None
    url: str | None = None
    external_id: str | None = None
    reference_id: str | None = None

    def toJson(self) -> str:
        jsondata = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        return jsondata

    def fromJson(content: str):
        return from_dict(ExternalReferenceMessage, content)
