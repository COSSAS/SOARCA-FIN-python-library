from typing import Optional
from soarca_fin_python_library.models.message import Message


class Unregister(Message):
    type: str = "unregister"
    # message_id: str implemented from parent
    capability_id: Optional[str] = None
    fin_id: Optional[str] = None
    all: bool = False
