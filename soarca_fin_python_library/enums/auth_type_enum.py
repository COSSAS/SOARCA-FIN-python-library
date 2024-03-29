from enum import Enum


class AuthTypeEnum(str, Enum):
    http_basic = "http-basic"
    oath2 = "oauth2"
    user_auth = "user-auth"
