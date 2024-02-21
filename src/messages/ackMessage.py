from dataclasses import dataclass

@dataclass
class AckMessage:
    type: str
    message_id: str