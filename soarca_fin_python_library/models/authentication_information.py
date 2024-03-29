from typing import Optional
from pydantic import BaseModel

from soarca_fin_python_library.enums.auth_type_enum import AuthTypeEnum


class AuthenticationInformation(BaseModel):
    id: str
    type: AuthTypeEnum
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
