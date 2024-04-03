from pydantic import BaseModel


class Meta(BaseModel):
    timestamp: str
    sender_id: str
