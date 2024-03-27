from typing import Optional
from pydantic import BaseModel

from src.models.authenticationInformation import AuthenticationInformation
from src.models.context import Context
from src.models.variable import Variable


class CommandSubStructure(BaseModel):
    command: str
    authentication: Optional[AuthenticationInformation] = None
    context: Context
    variables: Optional[dict[str, Variable]] = None
