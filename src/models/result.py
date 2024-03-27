from src.models.message import Message
from src.models.resultStructure import ResultStructure
from src.models.meta import Meta


class Result(Message):
    type: str = "result"
    # message_id: str implemented from parent
    result: ResultStructure
    meta: Meta
