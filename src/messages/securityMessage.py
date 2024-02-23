from dataclasses import dataclass


@dataclass
class SecurityMessage:
    version: str
    channel_security: str
