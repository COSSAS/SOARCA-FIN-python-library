from soarca_fin_python_library.models.message import Message
from soarca_fin_python_library.models.command_sub_structure import CommandSubStructure
from soarca_fin_python_library.models.meta import Meta


class Command(Message):
    type: str = "command"
    # message_id: str implemented from parent
    command: CommandSubStructure
    meta: Meta
