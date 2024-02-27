from typing import Optional
from pydantic import BaseModel

from enums.openVocabEnum import OpenVocabEnum


class AuthenticationInformation(BaseModel):
    type: OpenVocabEnum
    name: Optional[str]
    description: Optional[str]
    authentication_info_extensions: Optional[dict[str, str]]
