from dataclasses import dataclass
from messages.contextMessage import ContextMessage
from messages.variableMessage import VariableMessage


@dataclass
class CommandSubStructureMessage:
    command: str
    context: ContextMessage
    variables: dict[str, VariableMessage]
    authentication: any = None
