from dataclasses import dataclass


@dataclass
class ContextMessage:
    step_id: str
    playbook_id: str
    execution_id: str
    completed_on: str | None = None
    generated_on: str | None = None
    timeout: str | None = None
