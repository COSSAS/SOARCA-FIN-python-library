from pydantic import BaseModel
from src.enums.workFlowStepEnum import WorkFlowStepEnum
from src.models.agentStructure import AgentStructure
from src.models.stepStructure import StepStructure


class CapabilityStructure(BaseModel):
    capability_id: str
    type: WorkFlowStepEnum
    name: str
    version: str
    step: dict[str, StepStructure] = {}
    agent: dict[str, AgentStructure] = {}
