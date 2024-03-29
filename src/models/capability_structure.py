from pydantic import BaseModel
from src.enums.workflow_step_enum import WorkFlowStepEnum
from src.models.agent_structure import AgentStructure
from src.models.step_structure import StepStructure


class CapabilityStructure(BaseModel):
    capability_id: str
    type: WorkFlowStepEnum
    name: str
    version: str
    step: dict[str, StepStructure] = {}
    agent: dict[str, AgentStructure] = {}
