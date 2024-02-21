from dataclasses import dataclass


@dataclass
class UnRegisterMessage():
    type: str
    message_id: str
    capability_id: str
    fin_id: str
    all: bool
