from src.models.message import Message
from src.models.commandSubStructure import CommandSubStructure
from src.models.meta import Meta


class Command(Message):
    type: str = "command"
    # message_id: str implemented from parent
    command: CommandSubStructure
    meta: Meta
