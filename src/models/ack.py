
from src.models.message import Message


class Ack(Message):
    type: str = "ack"
    # message_id: str implemented from parent
