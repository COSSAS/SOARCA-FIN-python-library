
from models.message import Message


class Ack(Message):
    type: str = "ack"
