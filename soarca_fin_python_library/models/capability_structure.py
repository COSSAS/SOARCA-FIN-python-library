from pydantic import BaseModel
from soarca_fin_python_library.enums.workflow_step_enum import WorkFlowStepEnum
from soarca_fin_python_library.models.agent_structure import AgentStructure
from soarca_fin_python_library.models.step_structure import StepStructure


class CapabilityStructure(BaseModel):
    capability_id: str
    type: WorkFlowStepEnum
    name: str
    version: str
    step: dict[str, StepStructure] = {}
    agent: dict[str, AgentStructure] = {}
