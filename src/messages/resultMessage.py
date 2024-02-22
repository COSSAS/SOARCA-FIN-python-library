from dataclasses import dataclass

from messages.variableMessage import VariableMessage
from messages.resultStructure import ResultStructureMessage


@dataclass
class ResultMessage:
    message_id: str
    result: ResultStructureMessage
    variables: dict[str, VariableMessage]
    type: str = "result"
