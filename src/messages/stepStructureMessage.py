from dataclasses import dataclass
import json

from messages.extrernalReferenceMessage import ExternalReferenceMessage


@dataclass
class StepStructureMessage:
    type: str
    name: str
    description: str
    external_references: ExternalReferenceMessage
    command: str
    target: str
