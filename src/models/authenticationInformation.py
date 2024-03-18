from typing import Optional
from pydantic import BaseModel

from enums.openVocabEnum import OpenVocabEnum


class AuthenticationInformation(BaseModel):
    id: str
    type: OpenVocabEnum
    name: Optional[str] = None
    description: Optional[str] = None
    authentication_info_extensions: Optional[dict[str, str]] = None
    user_id: Optional[str] = None
    password: Optional[str] = None
    kms: Optional[bool] = None
    kms_key_identifier: Optional[str] = None
    username: Optional[str] = None
    oauth_header: Optional[str] = None
    token: Optional[str] = None
