from abc import ABC, abstractmethod

from soarca_fin_python_library.models.capability_structure import CapabilityStructure


class ISoarcaFin(ABC):

    @abstractmethod
    def set_config_MQTT_server(self, host: str, port: str, username: str, password: str) -> None:
        pass

    @abstractmethod
    def create_fin_capability(self, capability: CapabilityStructure, callback) -> None:
        pass

    @abstractmethod
    def start_fin(self) -> None:
        pass
