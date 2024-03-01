from models.message import Message
from enums.dispatcherTaskEnum import DispatcherTaskEnum
from models.result import Result


class DispatcherTask:

    def __init__(self, message: Message):
        self.state = DispatcherTaskEnum.WAITING
        self.result: Result = None
        self.message: Message = message

    def setState(self, state: DispatcherTaskEnum):
        self.state = state

    def setResult(self, result: Result = None):
        self.state = DispatcherTaskEnum.DONE
        self.result = result
