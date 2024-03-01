
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time
from models.message import Message
from handler import Handler
from models.register import Register
import logging as log
from models.unregister import Unregister
from dispatcherTask import DispatcherTask
from enums.dispatcherTaskEnum import DispatcherTaskEnum


class Dispatcher:

    def __init__(self, handler: Handler, max_workers: int = 1):
        self.handler = handler
        self.queue: Queue[Message] = Queue()
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self.current_tasks: dict[str, DispatcherTask] = {}

    def start_dispatcher(self):
        workers = self.thread_pool._max_workers
        for _ in range(workers):
            self.thread_pool.submit(self.start_worker_thread)

    def block_until_empty(self):
        self.queue.join()

    def block_until_task_done(self, message_id):
        try:
            task = self.current_tasks[message_id]
            while True:
                if task.state == DispatcherTaskEnum.DONE:
                    break
                time.sleep(0.1)
        except Exception as e:
            log.error(f"Task with {message_id} does not exist")

    def start_worker_thread(self):
        log.info("Started worker thread")
        while True:
            message = self.get_message()
            try:
                # pass message to handler
                log.info(f"New message {message}")
                match message:
                    case Register():
                        self.handler.register_fin(message)
                    case Unregister():
                        self.handler.unregister_fin(message)
                    case _:
                        log.error("Unkown message type")
            finally:
                task = self.current_tasks[message.message_id]
                task.setResult()
                self.queue.task_done()

    def add_message(self, message: Message) -> None:
        self.queue.put(message)
        task = DispatcherTask(message)
        self.current_tasks[message.message_id] = task

    def get_message(self) -> Message:
        message = self.queue.get()
        task = self.current_tasks[message.message_id]
        task.setState(DispatcherTaskEnum.RUNNING)
        return message
