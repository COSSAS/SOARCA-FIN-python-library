from pydantic import BaseModel
from src.models.external_reference import ExternalReference


class StepStructure(BaseModel):
    type: str = "action"
    name: str
    description: str
    external_references: ExternalReference
    command: str
    target: str
