from concurrent.futures import ThreadPoolExecutor
import paho.mqtt.client as mqtt


class Executor:

    def __init__(self, max_workers: int):
        self.thread_pool = ThreadPoolExecutor(max_workers=max_workers)
        self.current_tasks = []

    def submit(self, fn):
        task = self.thread_pool.submit(fn)
        self.current_tasks.append(task)
        task.add_done_callback(lambda x: self.current_tasks.remove(x))
        return task
