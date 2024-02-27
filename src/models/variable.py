from pydantic import BaseModel

from enums.variableTypeEnum import VariableTypeEnum


class Variable(BaseModel):
    type: VariableTypeEnum
    description: str
    value: str
    constant: bool
    external: bool
