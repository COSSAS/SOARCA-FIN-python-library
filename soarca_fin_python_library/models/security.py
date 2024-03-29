from pydantic import BaseModel


class Security(BaseModel):
    version: str
    channel_security: str