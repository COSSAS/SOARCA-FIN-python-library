from dataclasses import dataclass
import json


@dataclass
class StepStructureMessage:
    type: str
    name: str
    description: str
    external_references: any
    command: str
    target: str
