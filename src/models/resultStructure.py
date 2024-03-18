from pydantic import BaseModel

from src.models.context import Context
from src.models.variable import Variable


class ResultStructure(BaseModel):
    state: str
    context: Context
    variables: dict[str, Variable]