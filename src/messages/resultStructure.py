from dataclasses import dataclass

from messages.contextMessage import ContextMessage
from messages.variableMessage import VariableMessage


@dataclass
class ResultStructureMessage:
    state: str
    context: ContextMessage
    variables: dict[str, VariableMessage]
