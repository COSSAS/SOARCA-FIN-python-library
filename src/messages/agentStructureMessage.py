from dataclasses import dataclass


@dataclass
class AgentStructureMessage:
    type: str
    name: str
