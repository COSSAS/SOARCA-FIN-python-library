from click import Context
from models.message import Message
from models.commandSubStructure import CommandSubStructure
from models.meta import Meta


class Command(Message):
    type: str = "command"
    # message_id: str implemented from parent
    command: CommandSubStructure
    meta: Meta
