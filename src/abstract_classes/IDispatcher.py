from abc import ABC, abstractmethod


class IHandler(ABC):

    @abstractmethod
    def start_dispatcher() -> None:
        pass

    @abstractmethod
    def queue_message() -> None:
        pass
