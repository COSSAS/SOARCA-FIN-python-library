from enum import Enum


class WorkFlowStepEnum(str, Enum):
    start = "start"
    end = "end"
    action = "action"
    playbook_action = "playbook_action"
    parallel = "parallel"
    if_condition = "if-condition"
    while_condition = "while-condition"
    switch_conditon = "switch-condition"
