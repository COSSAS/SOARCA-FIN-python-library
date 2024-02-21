from dataclasses import dataclass


@dataclass
class NackMessage:
    type: str
    message_id: str
