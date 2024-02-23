import json
from dataclasses import dataclass

from dacite import from_dict


@dataclass
class AgentStructureMessage:
    name: str
    type: str = "soarca-fin"

    def toJson(self) -> str:
        jsondata = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        return jsondata
    
    def fromJson(content: str):
        return from_dict(AgentStructureMessage, content)
