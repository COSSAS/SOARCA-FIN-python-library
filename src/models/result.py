from models.message import Message
from models.resultStructure import ResultStructure
from models.meta import Meta


class Result(Message):
    type: str = "result"
    # message_id: str implemented from parent
    result: ResultStructure
    meta: Meta
