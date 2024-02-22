from dataclasses import dataclass


@dataclass
class VariableMessage:
    type: str
    description: str
    value: str
    constant: bool
    external: bool
