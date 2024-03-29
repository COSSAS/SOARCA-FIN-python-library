from pydantic import BaseModel


class Message(BaseModel):
    type: str
    message_id: str
