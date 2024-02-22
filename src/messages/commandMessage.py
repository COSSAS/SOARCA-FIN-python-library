from dataclasses import dataclass

from messages.metaMessage import MetaMessage
from messages.commandSubStructureMessage import CommandSubStructureMessage


@dataclass
class CommandMessage:
    message_id: str
    meta: MetaMessage
    command: CommandSubStructureMessage
    authentication_info: any | None = None
    type: str = "command"
