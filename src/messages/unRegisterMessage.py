import json
from dataclasses import dataclass


@dataclass
class UnRegisterMessage():
    message_id: str
    capability_id: str | None = None
    fin_id: str | None = None
    all: bool = False
    type: str = "unregister"

    def toJson(self) -> str:
        jsondata = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        return jsondata
