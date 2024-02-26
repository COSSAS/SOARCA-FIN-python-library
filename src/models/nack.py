
from models.message import Message


class Nack(Message):
    type: str = "nack"
