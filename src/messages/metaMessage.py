from dataclasses import dataclass


@dataclass
class MetaMessage:
    sender_id: str
    timestamp: str = ""
