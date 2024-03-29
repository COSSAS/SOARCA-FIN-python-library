from soarca_fin_python_library.models.message import Message


class Nack(Message):
    type: str = "nack"
    # message_id: str implemented from parent
