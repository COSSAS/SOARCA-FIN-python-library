from pydantic import BaseModel
import paho.mqtt.client as mqtt


class Task(BaseModel):
    id: str
    topic: str
    mqttc: mqtt.Client
    done_callback: function | None = None
    name: str = ""
