from pydantic import BaseModel
from typing import Optional
from enums.workFlowStepEnum import WorkFlowStepEnum
from models.agentStructure import AgentStructure
from models.stepStructure import StepStructure


class CapabilityStructure(BaseModel):
    capability_id: str
    type: WorkFlowStepEnum
    name: str
    version: str
    step: dict[str, StepStructure] = {}
    agent: dict[str, AgentStructure] = {}
