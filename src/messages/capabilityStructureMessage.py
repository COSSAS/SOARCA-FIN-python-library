from dataclasses import dataclass
import json
from messages.agentStructureMessage import AgentStructureMessage
from messages.stepStructureMessage import StepStructureMessage


@dataclass
class CapabilityStructureMessage:
    capability_id: str
    type: any
    name: str
    version: str
    step: StepStructureMessage
    agent: AgentStructureMessage

    def toJson(self) -> str:
        jsondata = json.dumps(self, default=lambda o: o.__dict__, indent=4)
        return jsondata
