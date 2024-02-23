import json
from dataclasses import dataclass

from messages.variableMessage import VariableMessage
from messages.resultStructure import ResultStructureMessage


@dataclass
class ResultMessage:
    message_id: str
    result: ResultStructureMessage
    variables: dict[str, VariableMessage]
    type: str = "result"

    def toJson(self) -> str:
            jsondata = json.dumps(self, default=lambda o: o.__dict__, indent=4)
            return jsondata