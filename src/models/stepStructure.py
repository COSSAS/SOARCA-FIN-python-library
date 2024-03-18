from pydantic import BaseModel
from models.externalReference import ExternalReference


class StepStructure(BaseModel):
    type: str = "action"
    name: str
    description: str
    external_references: ExternalReference
    command: str
    target: str
