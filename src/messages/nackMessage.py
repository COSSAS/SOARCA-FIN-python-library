import json
from dataclasses import dataclass

from dacite import from_dict


@dataclass
class NackMessage:
    message_id: str
    type: str = "nack"

    def toJson(self) -> str:
        jsondata = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        return jsondata

    def fromJson(content: str):
        return from_dict(NackMessage, content)
