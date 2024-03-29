from pydantic import BaseModel

from soarca_fin_python_library.enums.variable_type_enum import VariableTypeEnum


class Variable(BaseModel):
    type: VariableTypeEnum
    name: str
    description: str
    value: str
    constant: bool
    external: bool
