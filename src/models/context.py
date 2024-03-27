from typing import Optional
from pydantic import BaseModel


class Context(BaseModel):
    step_id: str
    playbook_id: str
    execution_id: str
    completed_on: Optional[str] = None
    generated_on: Optional[str] = None
    timeout: Optional[int] = None
