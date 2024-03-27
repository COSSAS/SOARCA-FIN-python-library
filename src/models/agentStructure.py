from pydantic import BaseModel


class AgentStructure(BaseModel):
    type: str = "soarca-fin"
    name: str
