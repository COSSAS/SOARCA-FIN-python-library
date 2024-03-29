from pydantic import BaseModel

from soarca_fin_python_library.models.context import Context
from soarca_fin_python_library.models.variable import Variable


class ResultStructure(BaseModel):
    state: str
    context: Context
    variables: dict[str, Variable]