from typing import Optional
from pydantic import BaseModel

from models.authenticationInformation import AuthenticationInformation
from models.context import Context
from models.variable import Variable


class CommandSubStructure(BaseModel):
    command: str
    authentication: Optional[dict[str, AuthenticationInformation]]
    context: Context
    variables: dict[str, Variable]
