from soarca_fin_python_library.models.message import Message
from soarca_fin_python_library.models.result_structure import ResultStructure
from soarca_fin_python_library.models.meta import Meta


class Result(Message):
    type: str = "result"
    # message_id: str implemented from parent
    result: ResultStructure
    meta: Meta
