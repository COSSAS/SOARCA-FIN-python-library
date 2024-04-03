from abc import ABC, abstractmethod

from soarca_fin_python_library.models.message import Message


class IExecutor(ABC):
    @abstractmethod
    def queue_message(self, message: Message) -> None:
        pass
