from enum import Enum


class WorkFlowStepEnum(Enum):
    START = 0
    END = 1
    ACTION = 2
    PLAYBOOK_ACTION = 3
    PARALLEL = 4
    IF_CONDITION = 5
    WHILE_CONDITION = 6
    SWITCH_CONDITION = 7
