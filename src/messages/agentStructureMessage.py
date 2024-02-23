import json
from dataclasses import dataclass


@dataclass
class AgentStructureMessage:
    name: str
    type: str = "soarca-fin"

    def toJson(self) -> str:
        jsondata = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        return jsondata
