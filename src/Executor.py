import time
from abstract_classes.IExecutor import IExecutor
from models.message import Message
from queue import Queue
from paho.mqtt.client import Client

from models.command import Command
from models.ack import Ack
import logging as log
from queue import Empty

from models.result import Result
from models.nack import Nack
from models.register import Register


class Executor(IExecutor):

    def __init__(self, id: str, callback, queue: Queue, mqttc: Client):
        self.queue: Queue[Message] = queue
        self.mqttc: Client = mqttc
        self.id = id
        self.callback = callback
        self.TIMEOUT = 30

    def queue_message(self, message: Message) -> None:
        self.queue.put(message)

    def start_executor(self):
        while True:
            # This method is blocking
            message = self._get_message_from_queue()

            match message:
                case Ack():
                    self._put_message_in_queue(message)
                case Nack():
                    self._put_message_in_queue(message)
                case Register():
                    self._handle_register_message(message)
                case Command():
                    self._handle_command_message(message)
                case _:
                    # Send Nack?
                    log.warn(
                        f"Unimplemented command: {message.model_dump_json()}")

    # Is blocking
    def _get_message_from_queue(self, timeout: float = None) -> Message:
        return self.queue.get(timeout=timeout)

    def _put_message_in_queue(self, message: Message, timeout: float = None):
        self.queue.put(message, timeout=timeout)

    def _handle_register_message(self, message: Register): \
            # Send command message to soarca
        self._send_message_as_json(message, topic="soarca")

        # Wait for ack
        retries = 3
        while retries > 0:
            try:
                self._wait_for_ack(message.message_id)
                break
            except (Empty, TimeoutError) as e:
                retries -= 1
                if retries == 0:
                    break
                self._send_message_as_json(message, topic="soarca")
            except RuntimeError as e:
                retries -= 1
                if retries == 0:
                    break
                self._send_message_as_json(message, topic="soarca")

    def _handle_command_message(self, message: Command):
        # Send ack back
        ack = Ack(message_id=message.message_id)
        self._send_message_as_json(ack)

        # Do Callback method

        result: Result = self.callback(message)

        # Send result back
        self._send_message_as_json(result)

        # Wait for ack
        retries = 3
        while retries > 0:
            try:
                self._wait_for_ack(result.message_id)
                break
            except (Empty, TimeoutError) as e:
                retries -= 1
                if retries == 0:
                    break
                self._send_message_as_json(result)
            except RuntimeError as e:
                retries -= 1
                if retries == 0:
                    break
                self._send_message_as_json(result)

    def _send_message_as_json(self, message: Message, topic: str = None):
        json_message = message.model_dump_json()
        if topic:
            self.mqttc.publish(topic, payload=json_message)
        else:
            self.mqttc.publish(self.id, payload=json_message)

    def _wait_for_ack(self, message_id: str):
        startTime = time.time()
        while time.time() < startTime + self.TIMEOUT:
            try:
                message = self._get_message_from_queue(timeout=self.TIMEOUT)
                while message.message_id != message_id:
                    timeout = self.TIMEOUT - (startTime - time.time())
                    self._put_message_in_queue(message, timeout=timeout)

                    message = self._get_message_from_queue(timeout=timeout)

                match message:
                    case Ack():
                        log.info(f"Receive ack for message {message_id}")
                        return
                    case Nack():
                        log.warn(f"Receive nack for message {message_id}")
                        raise RuntimeError("Receive a nack")
                    case _:
                        raise TypeError(
                            f"Unexpected message type {message.model_dump_json()}")

            except Empty as e:
                log.warn("Did not receive an ack")
                raise e

        raise TimeoutError(f"Timeout for message with id {message_id}")
