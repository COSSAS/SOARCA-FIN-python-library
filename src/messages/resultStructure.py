from dataclasses import dataclass


@dataclass
class ResultStructureMessage:
    result: any
    type: str = "result"