from typing import Optional
from pydantic import BaseModel

from soarca_fin_python_library.models.authentication_information import AuthenticationInformation
from soarca_fin_python_library.models.context import Context
from soarca_fin_python_library.models.variable import Variable


class CommandSubStructure(BaseModel):
    command: str
    authentication: Optional[AuthenticationInformation] = None
    context: Context
    variables: Optional[dict[str, Variable]] = None
