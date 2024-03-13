from abc import ABC, abstractmethod

from src.models.capabilityStructure import CapabilityStructure


class IMQTTClient(ABC):

    @abstractmethod
    def set_config_MQTT_server(host: str, port: str, username: str, password: str) -> None:
        pass

    @abstractmethod
    def set_fin_capabilitites(capabilities: list[CapabilityStructure]) -> None:
        pass

    @abstractmethod
    def start_fin() -> None:
        pass
