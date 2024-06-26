from datetime import datetime, timezone
import time
from uuid import uuid1
from soarca_fin_python_library.abstract_classes.i_executor import IExecutor
from soarca_fin_python_library.models.message import Message
from queue import Queue
from paho.mqtt.client import Client

from soarca_fin_python_library.models.command import Command
from soarca_fin_python_library.models.ack import Ack
import logging as log
from queue import Empty

from soarca_fin_python_library.models.result import Result
from soarca_fin_python_library.models.nack import Nack
from soarca_fin_python_library.models.register import Register
from soarca_fin_python_library.models.unregister import Unregister
from soarca_fin_python_library.models.unregister_self import UnregisterSelf
from soarca_fin_python_library.models.result_structure import ResultStructure
from soarca_fin_python_library.models.meta import Meta


class Executor(IExecutor):

    def __init__(self, executor_id: str, callback, queue: Queue, mqttc: Client):
        self.queue: Queue[Message] = queue
        self.mqttc: Client = mqttc
        self.acks: list[str] = []
        self.id = executor_id
        self.callback = callback
        self.TIMEOUT = 30
        self.running = True

    # Add message to queue.
    def queue_message(self, message: Message) -> None:
        self.queue.put(message)

    # Stop the executor by stoping the queue polling.
    def stop_executor(self):
        self.running = False

    # Main executor loop. Polls for messages in the queue and parsers them.
    def start_executor(self):

        log.info("Thread started for %s", self.id)
        self.running = True

        while self.running:
            try:
                # This method is blocking
                message = self._get_message_from_queue(timeout=10)
                match message:
                    case Ack() | Nack():
                        # Check if we are expecting this (n)ack
                        if message.message_id in self.acks:
                            self._put_message_in_queue(message)
                        else:
                            log.debug(
                                "Received unknown (n)ack with message_id: %s", message.message_id)
                    case Register():
                        self._handle_register_message(message)
                    case Unregister():
                        self._handle_unregister_message(message)
                    case UnregisterSelf():
                        self._handle_unregister_self_message(message)
                    case Command():
                        self._handle_command_message(message)
                    case _:
                        # Send Nack?
                        log.warning(
                            "Unimplemented command: %s", message.model_dump_json())
            except Empty:
                pass

        log.info("Thread ended for %s", self.id)

    # Gets message form queue. Is blocking.
    def _get_message_from_queue(self, timeout: float = None) -> Message:
        return self.queue.get(timeout=timeout)

    # Helper functtion to put messages in the queue with a timeout.
    def _put_message_in_queue(self, message: Message, timeout: float = None):
        self.queue.put(message, timeout=timeout)

    # Handles Unregister messages from SOARCA.
    # First sends an acknowledgement, then calls controll callback function to
    # stop fin(s).
    def _handle_unregister_message(self, message: Unregister):
        ack = Ack(message_id=message.message_id)
        self._send_message_as_json(ack, topic="soarca")

        self.callback(message)

    # Handles unregister messages if self generated.
    # Waits for an acknowledgement before calling controll callback function
    # to stop fin(s).
    def _handle_unregister_self_message(self, message: UnregisterSelf):
        # Send command message to soarca
        self._send_message_as_json(message, topic="soarca")

        # Wait for ack
        retries = 3
        while retries > 0:
            try:
                self._wait_for_ack(message.message_id)
                self.callback(message)
                return
            except (Empty, TimeoutError) as e:
                log.debug(e)
                self._send_message_as_json(message, topic="soarca")
            except RuntimeError as e:
                log.debug(e)
                self._send_message_as_json(message, topic="soarca")
            finally:
                retries -= 1
                if retries == 0:
                    log.fatal(
                        "Did not receive an ack for message %s. Aborting...", message.message_id)
                    exit(-1)

    # Handles self generated register message.
    # First sends a register message, then waits for acks.
    # If there is no successful acknowledgement, exit.
    def _handle_register_message(self, message: Register):
        # Send command message to soarca
        self._send_message_as_json(message, topic="soarca")

        # Wait for ack and retry 3 times
        retries = 3
        while retries > 0:
            try:
                # Send Ack and wait for a response
                self._wait_for_ack(message.message_id)
                return
            # Did not get a response in time
            except (Empty, TimeoutError) as e:
                log.debug(e)
                # Resend message
                self._send_message_as_json(message, topic="soarca")

            # Receive a response but the message failed (Nack)
            except RuntimeError:
                log.debug(e)
                # Resend message
                self._send_message_as_json(message, topic="soarca")
            finally:
                retries -= 1
                if retries == 0:
                    log.fatal(
                        "Did not receive an ack for message %s. Aborting...", message.message_id)
                    exit(-1)

    # Handles a command message from SOARCA.
    # First sends an acknowledgement back, then calls capability callback function with the command as argument.
    # Callback should return a result.
    # Send result back to SOARCA and wait for an acknowledgement
    def _handle_command_message(self, message: Command):
        # Send ack back
        ack = Ack(message_id=message.message_id)
        self._send_message_as_json(ack)

        # Do Callback method
        resultStruct: ResultStructure = self.callback(message)
        message_id = str(uuid1())
        timestamp = datetime.now(timezone.utc).isoformat()
        meta = Meta(timestamp=timestamp, sender_id=self.id)
        result = Result(message_id=message_id, meta=meta,
                        result=resultStruct)

        # Send result back
        self._send_message_as_json(result)

        # Wait for ack
        retries = 3
        while retries > 0:
            try:
                self._wait_for_ack(result.message_id)
                break
            except (Empty, TimeoutError) as e:
                log.debug(e)
                self._send_message_as_json(result)
            except RuntimeError as e:
                log.debug(e)
                self._send_message_as_json(result)
            finally:
                retries -= 1
            if retries == 0:
                self.acks.remove(message_id)
                log.error(
                    "Did not receive an acknowledgement for message %s. Skipping message...", result.message_id)
                break

    # Publishes a message as JSON on a topic. Default topic is self.id.
    def _send_message_as_json(self, message: Message, topic: str = None):
        json_message = message.model_dump_json()
        if topic:
            self.mqttc.publish(topic, payload=json_message)
        else:
            self.mqttc.publish(self.id, payload=json_message)

    # Helper function to wait for acknowledgements.
    # Polls message queue for acks and nacks. If message is not for the correct one, retrieve new message from queue and put the old message back in.
    # If timeout expires or a nack is received, raise an exception.
    def _wait_for_ack(self, message_id: str):
        # Notify executor that we are waiting for an ack
        self.acks.append(message_id)
        startTime = time.time()
        while time.time() < startTime + self.TIMEOUT:
            try:
                message = self._get_message_from_queue(timeout=self.TIMEOUT)
                while message.message_id != message_id:
                    timeout = self.TIMEOUT - (startTime - time.time())
                    self._put_message_in_queue(message, timeout=timeout)

                    message = self._get_message_from_queue(timeout=timeout)

                # Notify executor that we received ack
                self.acks.remove(message_id)
                match message:
                    case Ack():
                        log.info("Received ack for message: %s", message_id)
                        return
                    case Nack():
                        log.warning(
                            "Received nack for message: %s", message_id)
                        raise RuntimeError("Received a nack")
                    case _:
                        raise TypeError(
                            f"Unexpected message type {message.model_dump_json()}")

            except Empty as e:
                log.warning("Did not receive an ack")
                raise e

        raise TimeoutError(f"Timeout for message with id {message_id}")
