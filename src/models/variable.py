from pydantic import BaseModel

from src.enums.variableTypeEnum import VariableTypeEnum


class Variable(BaseModel):
    type: VariableTypeEnum
    name: str
    description: str
    value: str
    constant: bool
    external: bool
