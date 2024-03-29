from abc import ABC, abstractmethod

from src.models.message import Message


class IExecutor(ABC):

    @abstractmethod
    def queue_message(self, message: Message) -> None:
        pass
