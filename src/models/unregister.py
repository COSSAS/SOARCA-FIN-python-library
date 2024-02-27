from typing import Optional
from models.message import Message


class Unregister(Message):
    type: str = "unregister"
    # message_id: str implemented from parent
    capability_id: Optional[str]
    fin_id: Optional[str]
    all: bool
