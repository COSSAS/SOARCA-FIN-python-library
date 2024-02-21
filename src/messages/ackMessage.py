import json
from dataclasses import dataclass

@dataclass
class AckMessage:
    message_id: str
    type: str = "ack"

    def toJson(self) -> str:
        jsondata = json.dumps(self, default=lambda o:o.__dict__, indent=4)
        return jsondata