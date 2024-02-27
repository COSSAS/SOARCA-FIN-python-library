from pydantic import BaseModel

from models.context import Context
from models.variable import Variable


class ResultStructure(BaseModel):
    state: str
    context: Context
    variables: dict[str, Variable]