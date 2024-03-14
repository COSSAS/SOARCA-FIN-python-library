from abc import ABC, abstractmethod

from models.message import Message


class IExecutor(ABC):

    @abstractmethod
    def queue_message(self, message: Message) -> None:
        pass
