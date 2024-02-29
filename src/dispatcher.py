
from concurrent.futures import ThreadPoolExecutor
import time
from queue import Queue
from models.message import Message
from handler import Handler
from models.register import Register
import logging as log

from models.unregister import Unregister


class Dispatcher:

    def __init__(self, handler: Handler, max_workers: int = 1):
        self.handler = handler
        self.queue: Queue[Message] = Queue()
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self.current_tasks = []

    def start_dispatcher(self):
        workers = self.thread_pool._max_workers
        for i in range(workers):
            self.thread_pool.submit(self.start_worker_thread)

    def start_worker_thread(self):
        log.info("Started worker thread")
        while True:
            message = self.get_message()
            # pass message to handler
            log.info(f"New message {message}")
            match message:
                case Register():
                    self.handler.register_fin(message)
                case Unregister():
                    self.handler.unregister_fin(message)
                case _:
                    log.error("Unkown message type")
            # if return value, add to queue
            self.queue.task_done()
            time.sleep(0.1)

    def add_message(self, message: Message) -> None:
        self.queue.put(message)

    def get_message(self) -> Message:
        message = self.queue.get()
        return message
